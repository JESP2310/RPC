# services/service_busca.py
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.server_rpc import start_rpc_server

SERVICE_NAME = "rpc_busca"

DADOS = [
    "Python básico",
    "Node.js avançado",
    "Estruturas de dados",
    "Segurança da informação",
    "Sistemas distribuídos"
]

def busca(data):
    print(f"[→] Requisição recebida no serviço rpc_busca: {data}")

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return {"error": f"Erro ao interpretar JSON: {e}"}

    if isinstance(data, dict):
        termo = data.get("termo", "")
        if not termo:
            return {"error": "Nenhum termo informado."}

        resultado = [item for item in DADOS if termo.lower() in item.lower()]
        print(f"→ BUSCA realizada com sucesso: {resultado}")
        return {"result": resultado}

    return {"error": "Formato de dados inválido"}

if __name__ == "__main__":
    print(f"[RPC SERVER] Aguardando requisições no serviço '{SERVICE_NAME}'...")
    start_rpc_server(SERVICE_NAME, busca)
