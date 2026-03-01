from web3 import Web3

# 1. Definimos el "puente" hacia la blockchain. 
# Usaremos un nodo público y gratuito de Cloudflare para conectarnos a la red principal de Ethereum.
NODO_RPC = "https://eth.llamarpc.com"

# 2. Inicializamos la conexión
w3 = Web3(Web3.HTTPProvider(NODO_RPC))

# 3. Verificamos si logramos entrar
print("Iniciando conexión forense...")

if w3.is_connected():
    print("✅ ¡Conexión exitosa a la Blockchain!")
    
    # Extraemos nuestro primer dato en vivo: el último bloque minado
    ultimo_bloque = w3.eth.block_number
    print(f"📦 El bloque más reciente en la red es: {ultimo_bloque}")
    
    # Podemos ver un poco más de información de ese bloque
    datos_bloque = w3.eth.get_block('latest')
    print(f"⏱️  Timestamp del bloque: {datos_bloque['timestamp']}")
    print(f"⛽ Gas usado en este bloque: {datos_bloque['gasUsed']}")
    
else:
    print("❌ Error: No se pudo conectar al nodo.")