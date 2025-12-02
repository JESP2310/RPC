# services/service_media.py
import sys
import os
import json

# Adiciona o diretório pai ao sys.path para conseguir importar 'server'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.server_rpc import start_rpc_server

SERVICE_NAME = "rpc_media"

def media(data):
    print(f"[→] Requisição recebida no serviço rpc_media: {data}")

    # Caso venha como string JSON
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"Erro ao interpretar JSON: {e}"

    # Caso venha como dicionário
    if isinstance(data, dict):
        numeros = data.get("valores")
        if not numeros or not isinstance(numeros, list):
            return "Formato de dados inválido. Envie uma lista de números."
        resultado = sum(numeros) / len(numeros)
        print(f"→ MÉDIA recebida (JSON): {numeros} → Resultado: {resultado}")
        return str(resultado)

    return "Formato de dados inválido"

if __name__ == "__main__":
    print(f"[RPC SERVER] Aguardando requisições no serviço '{SERVICE_NAME}'...")
    start_rpc_server(SERVICE_NAME, media)
