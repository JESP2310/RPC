# services/service_soma.py
import sys
import os
import json

# Adiciona o diretório pai ao sys.path para conseguir importar 'server'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.server_rpc import start_rpc_server

SERVICE_NAME = "rpc_soma"

def soma(data):
    print(f"[→] Requisição recebida no serviço rpc_soma: {data}")

    # Caso venha como string "2,3"
    if isinstance(data, str):
        try:
            partes = data.split(",")
            a = int(partes[0])
            b = int(partes[1])
            print(f"→ SOMA recebida (string): {a} + {b}")
            return str(a + b)
        except Exception as e:
            return f"Erro ao interpretar string: {e}"

    # Caso venha como JSON {"a": 10, "b": 20}
    if isinstance(data, dict):
        a = data.get("a")
        b = data.get("b")
        print(f"→ SOMA recebida (JSON): {a} + {b}")
        return str(a + b)

    return "Formato de dados inválido"

if __name__ == "__main__":
    print(f"[RPC SERVER] Aguardando requisições no serviço '{SERVICE_NAME}'...")
    start_rpc_server(SERVICE_NAME, soma)
