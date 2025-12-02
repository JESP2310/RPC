# server/server_rpc.py
import pika
import json
import traceback

def start_rpc_server(queue_name, process_function):
    """
    Inicia um servidor RPC que consome a fila `queue_name`.
    process_function(data: dict) -> Any
    - aceita JSON válido enviado pelo cliente (ex: {"a": 2, "b": 3})
    - aceita payload no formato "2,3" (string)
    - aceita payload no formato '"2,3"' (string com aspas)
    A resposta é empacotada em JSON: {"result": <valor>}
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    print(f"[RPC SERVER] Aguardando requisições no serviço '{queue_name}'...")

    def callback(ch, method, props, body):
        raw = body.decode()
        print(f"[→] Requisição recebida no serviço {queue_name}: {raw}")

        # Tenta interpretar JSON primeiro
        data = None
        try:
            data = json.loads(raw)
        except Exception:
            # Remove aspas externas se houver
            raw_stripped = raw.strip()
            if (raw_stripped.startswith('"') and raw_stripped.endswith('"')) or \
               (raw_stripped.startswith("'") and raw_stripped.endswith("'")):
                raw_stripped = raw_stripped[1:-1]

            # Se for "a,b" -> converte para {"a": int(a), "b": int(b)}
            if "," in raw_stripped:
                try:
                    a_str, b_str = raw_stripped.split(",", 1)
                    a = int(a_str.strip())
                    b = int(b_str.strip())
                    data = {"a": a, "b": b}
                except Exception:
                    # fallback: passa como string no campo "value"
                    data = {"value": raw_stripped}
            else:
                # fallback genérico
                data = {"value": raw_stripped}

        try:
            result = process_function(data)
        except Exception as e:
            # Em caso de erro no processamento, envie um erro legível
            tb = traceback.format_exc()
            print("Erro ao executar process_function:\n", tb)
            response_payload = {"error": str(e), "trace": tb}
        else:
            response_payload = {"result": result}

        response_body = json.dumps(response_payload)

        # Publica resposta para o cliente (reply_to + correlation_id)
        try:
            ch.basic_publish(
                exchange="",
                routing_key=props.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id
                ),
                body=response_body,
            )
        except Exception as e:
            print("Erro ao publicar resposta:", e)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(f"[RPC SERVER] Servidor '{queue_name}' iniciado!")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[RPC SERVER] Interrompido pelo usuário. Encerrando...")
    finally:
        try:
            if channel.is_open:
                channel.close()
            if connection.is_open:
                connection.close()
        except Exception:
            pass
