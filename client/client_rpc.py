# client/client_rpc.py
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.rpc_utils import RpcClientBase

SERVICOS = {
    "1": "rpc_soma",
    "2": "rpc_media",
    "3": "rpc_busca"
}

def menu():
    print("\n=== MENU DE SERVIÇOS RPC ===")
    print("1 - Soma")
    print("2 - Média")
    print("3 - Busca")
    print("0 - Sair")
    return input("Escolha um serviço: ")

def solicitar_parametros(servico):
    if servico == "rpc_soma":
        entrada = input("Digite dois números separados por vírgula (ex: 10,20): ")
        return entrada.strip()
    elif servico == "rpc_media":
        entrada = input("Digite números separados por vírgula (ex: 10,20,30): ")
        try:
            valores = [float(x.strip()) for x in entrada.split(",")]
            return json.dumps({"valores": valores})
        except:
            print("Formato inválido!")
            return None
    elif servico == "rpc_busca":
        termo = input("Digite o termo para busca: ")
        return json.dumps({"termo": termo.strip()})

def main():
    client = RpcClientBase()

    while True:
        opcao = menu()

        if opcao == "0":
            print("Saindo...")
            break

        servico = SERVICOS.get(opcao)
        if not servico:
            print("Opção inválida. Tente novamente.")
            continue

        parametros = solicitar_parametros(servico)
        if parametros is None:
            continue

        try:
            resposta = client.call(servico, parametros)
            # decodifica JSON retornado pelo servidor
            resposta_json = json.loads(resposta)
            if "result" in resposta_json:
                print(f"Resultado do serviço '{servico}': {resposta_json['result']}")
            else:
                print(f"Erro do serviço '{servico}': {resposta_json.get('error')}")
        except Exception as e:
            print(f"Erro ao chamar o serviço: {e}")

if __name__ == "__main__":
    main()
