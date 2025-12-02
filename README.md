# Sistema RPC com RabbitMQ

## Descrição do Projeto

Este projeto implementa um sistema distribuído de serviços via **RPC (Remote Procedure Call)** utilizando **RabbitMQ** como broker de mensagens.

O sistema permite que múltiplos serviços sejam acessados por um cliente, demonstrando:

* **Comunicação assíncrona** entre cliente e servidor.
* **Distribuição de tarefas** entre serviços.
* **Mecanismo de request/response** via RabbitMQ (RPC).

### Componentes

1. **Serviços** (`services/`):

   * `service_soma.py` → soma dois números.
   * `service_media.py` → calcula a média de uma lista de números.
   * `service_busca.py` → busca um termo em uma base de dados simulada.

2. **Cliente** (`client/client_rpc.py`)
   Menu interativo para chamar qualquer serviço.

3. **Servidor RPC base** (`server/server_rpc.py`)
   Implementa a lógica de RPC para os serviços.

---

## Comunicação assíncrona

Cada serviço funciona **de forma independente** e processa mensagens do RabbitMQ sem bloquear outros serviços.
O cliente envia uma requisição e espera a resposta, mas **cada serviço pode processar várias requisições simultaneamente**, demonstrando comunicação assíncrona.

---

## Distribuição de tarefas

O RabbitMQ distribui automaticamente as requisições entre instâncias de serviços idênticos se existirem múltiplos consumidores, permitindo **balanceamento de carga**.

Exemplo:

* Duas instâncias de `service_soma.py` rodando no mesmo broker → o RabbitMQ envia requisições alternadamente entre elas.

---

## Mecanismo RPC

O cliente utiliza o padrão **request/response** do RabbitMQ:

1. Cliente envia mensagem para a fila do serviço desejado.
2. Serviço processa a mensagem e envia a resposta para a **callback queue** do cliente.
3. Cliente recebe a resposta e apresenta o resultado ao usuário.

Implementado através da classe `RpcClientBase` em `common/rpc_utils.py`.

---

## Como executar cada componente

### Pré-requisitos

* Python 3.10+
* RabbitMQ instalado e rodando localmente (`localhost`)
* Dependências Python:

```bash
pip install pika
```

### Executando os serviços

Abra um terminal para cada serviço:

* **Terminal 1** (Soma):

```bash
python services/service_soma.py
```

* **Terminal 2** (Média):

```bash
python services/service_media.py
```

* **Terminal 3** (Busca):

```bash
python services/service_busca.py
```

### Executando o cliente

Abra outro terminal e rode o cliente:

```bash
python -m client.client_rpc
```

O cliente exibirá o seguinte menu interativo:

```text
=== MENU DE SERVIÇOS RPC ===
1 - Soma
2 - Média
3 - Busca
0 - Sair
Escolha um serviço:
```

O usuário poderá escolher o serviço e fornecer os parâmetros solicitados.

---

## Fluxo esperado de funcionamento

1. Cliente seleciona um serviço e envia os parâmetros para a fila correspondente no RabbitMQ.
2. O serviço consome a mensagem da fila, processa os dados e envia a resposta para a callback queue do cliente.
3. O cliente recebe a resposta e imprime o resultado na tela.
4. Outros serviços continuam processando requisições de forma assíncrona.

---

## Exemplos de saída

### Soma

```text
Escolha um serviço: 1
Digite dois números separados por vírgula (ex: 10,20): 23,10
Resultado do serviço 'rpc_soma': 33
```

### Média

```text
Escolha um serviço: 2
Digite números separados por vírgula (ex: 10,20,30): 5,10,15
Resultado do serviço 'rpc_media': 10.0
```

### Busca

```text
Escolha um serviço: 3
Digite o termo para busca: Python
Resultado do serviço 'rpc_busca': ['Python básico']
```

---

## Estrutura de diretórios

```text
C:.
│   requirements.txt
│   
├───client
│       client_rpc.py
│       __init__.py
│       
├───common
│       rpc_utils.py
│       __init__.py
│
├───server
│       server_rpc.py
│
└───services
        service_soma.py
        service_media.py
        service_busca.py
        __init__.py
```

---

## Observações

* Todos os serviços retornam **dicionários** com chave `"result"` para evitar JSON duplo.
* O cliente decodifica a resposta e apresenta apenas o resultado final.
* É possível rodar múltiplas instâncias de um mesmo serviço para demonstrar **balanceamento de carga**.

