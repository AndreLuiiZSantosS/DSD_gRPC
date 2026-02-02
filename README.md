# Monitoramento Financeiro via gRPC

Projeto desenvolvido para a disciplina de Sistemas Distribuídos.
O objetivo é demonstrar a comunicação eficiente entre microsserviços utilizando **gRPC (Google Remote Procedure Call)** e **Streaming de Dados** entre linguagens diferentes.

## 🛠️ Tecnologias e Arquitetura

* **Protocolo:** gRPC (HTTP/2 + Protocol Buffers).
* **Servidor:** Python (Gera cotações simuladas de ativos em tempo real).
* **Cliente:** Node.js (Consome o stream e exibe no terminal formatado).
* **Contrato:** `cotacao.proto` (Define a estrutura dos dados binários).

## Como Rodar o Projeto

### Pré-requisitos
* Python 3.x
* Node.js

### 1. Instalação
No terminal, dentro da pasta do projeto:

```bash
# Instalar dependências do Servidor (Python)
pip install grpcio grpcio-tools

# Instalar dependências do Cliente (Node.js)
npm install