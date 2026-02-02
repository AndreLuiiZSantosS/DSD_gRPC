import grpc
from concurrent import futures
import time
import random
from datetime import datetime

# Estes imports vão dar erro agora, mas funcionarão depois que rodar o comando de compilação
import cotacao_pb2
import cotacao_pb2_grpc

class ServicoBolsa(cotacao_pb2_grpc.BolsaValoresServicer):
    def MonitorarPrecos(self, request, context):
        print(f"[SERVER] Novo Investidor conectado! Iniciando stream...")
        
        moedas = ["BITCOIN", "ETHEREUM", "DOLLAR", "EURO"]
        
        # Loop infinito que envia dados (Streaming)
        while True:
            # Se o cliente desconectar, para o loop
            if not context.is_active():
                print("[SERVER] Cliente desconectou.")
                break

            # 1. Gera dados aleatórios
            item = random.choice(moedas)
            if item == "BITCOIN":
                preco = random.uniform(40000, 42000)
            elif item == "ETHEREUM":
                preco = random.uniform(2800, 3100)
            else:
                preco = random.uniform(5, 6) # Moedas fiat
            
            agora = datetime.now().strftime("%H:%M:%S")

            # 2. Empacota no formato do Proto
            resposta = cotacao_pb2.Cotacao(
                moeda=item,
                valor=round(preco, 2),
                timestamp=agora
            )

            # 3. Envia para o cliente (Yield mantém a conexão aberta)
            yield resposta
            
            # Simula a velocidade do mercado (0.1s a 1s)
            time.sleep(random.uniform(0.1, 1.0))

def rodar_servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cotacao_pb2_grpc.add_BolsaValoresServicer_to_server(ServicoBolsa(), server)
    
    # Roda na porta 50051 (Padrão do gRPC)
    server.add_insecure_port('[::]:50051')
    print("="*40)
    print("  SERVIDOR BOLSA DE VALORES (PYTHON) ONLINE")
    print("    Porta: 50051 | Aguardando Node.js...")
    print("="*40)
    
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    rodar_servidor()