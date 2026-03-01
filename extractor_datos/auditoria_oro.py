from web3 import Web3
from supabase import create_client, Client

# --- CREDENCIALES DE TU BÓVEDA EN LA NUBE (SUPABASE) ---
SUPABASE_URL = "https://cxydeqwjpbeueezsunpm.supabase.co"
SUPABASE_KEY = "sb_publishable_IqyYnVgSLraKOdowjreh0Q_L1kpRvUr"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PUENTE A LA BLOCKCHAIN ---
NODO_RPC = "https://eth.drpc.org"
w3 = Web3(Web3.HTTPProvider(NODO_RPC))

if w3.is_connected():
    print("✅ Conexión exitosa a la Blockchain")
    
    # 1. AUDITORÍA PAXG
    paxg_address = w3.to_checksum_address("0x45804880De22913dAFE09f4980848ECE6EcbAf78")
    paxg_abi = [
        {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
    ]
    contrato_paxg = w3.eth.contract(address=paxg_address, abi=paxg_abi)
    print("🔍 Extrayendo reservas físicas de PAX Gold...")
    
    decimales_paxg = contrato_paxg.functions.decimals().call()
    onzas_reales = float(contrato_paxg.functions.totalSupply().call() / (10 ** decimales_paxg))
    
    # 2. ORÁCULO DE PRECIOS CHAINLINK
    chainlink_address = w3.to_checksum_address("0x214eD9Da11D2fbe465a6fc601a91E62EbEc1a0D6")
    chainlink_abi = [
        {"inputs": [], "name": "latestRoundData", "outputs": [{"name": "roundId", "type": "uint80"}, {"name": "answer", "type": "int256"}, {"name": "startedAt", "type": "uint256"}, {"name": "updatedAt", "type": "uint256"}, {"name": "answeredInRound", "type": "uint80"}], "stateMutability": "view", "type": "function"},
        {"inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}
    ]
    contrato_oraculo = w3.eth.contract(address=chainlink_address, abi=chainlink_abi)
    print("📡 Consultando precio en vivo al oráculo...")
    
    decimales_precio = contrato_oraculo.functions.decimals().call()
    precio_oro_usd = float(contrato_oraculo.functions.latestRoundData().call()[1] / (10 ** decimales_precio))
    
    # 3. CÁLCULO
    valor_total_boveda = float(onzas_reales * precio_oro_usd)
    
    # 4. INYECCIÓN A LA BASE DE DATOS
    print("☁️  Inyectando reporte en Supabase...")
    try:
        respuesta = supabase.table('auditorias_paxg').insert({
            "onzas_totales": onzas_reales,
            "precio_usd": precio_oro_usd,
            "valor_total_boveda": valor_total_boveda
        }).execute()
        print("💾 ¡Inyección exitosa! Los datos están seguros en la nube.")
    except Exception as e:
        print(f"❌ Error al guardar en Supabase: {e}")
        
    print("-" * 50)
    print(f"🏦 VALOR REGISTRADO: ${valor_total_boveda:,.2f} USD")
    print("-" * 50)
    
else:
    print("❌ Error de conexión al nodo RPC.")