const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// 1. Carrega o arquivo .proto dinamicamente
const PROTO_PATH = path.join(__dirname, 'cotacao.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});
// Carrega o pacote 'financeiro' definido no proto
const proto = grpc.loadPackageDefinition(packageDefinition).financeiro;

// 2. Conecta no servidor Python (localhost:50051)
const client = new proto.BolsaValores('localhost:50051', grpc.credentials.createInsecure());

console.log("========================================");
console.log("  TERMINAL DO INVESTIDOR (NODE.JS)");
console.log("    Conectando ao Servidor Python...");
console.log("========================================");

// 3. Inicia o Stream (Chama a função remota)
const stream = client.MonitorarPrecos({});

// 4. Fica ouvindo os dados chegarem ('data')
stream.on('data', function(dado) {
    let cor = "\x1b[37m"; // Branco padrão
    let icone = "💵";

    // Lógica visual (Cores de Terminal)
    if(dado.moeda === "BITCOIN") { 
        cor = "\x1b[33m"; // Amarelo
        icone = "₿";
    }
    if(dado.moeda === "ETHEREUM") {
        cor = "\x1b[36m"; // Ciano
        icone = "Ξ";
    }
    if(dado.moeda === "DOLLAR") {
        cor = "\x1b[32m"; // Verde
        icone = "$";
    }

    console.log(`${cor}[${dado.timestamp}] ${icone} ${dado.moeda}: ${dado.valor.toFixed(2)}\x1b[0m`);
});

stream.on('end', () => console.log('Pregão encerrado.'));
stream.on('error', (e) => console.error("Erro de Conexão:", e.details));