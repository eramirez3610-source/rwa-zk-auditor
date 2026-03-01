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
    print("✅ Conexión exitosa a la Blockchain\n")
    
    # 1. AUDITORÍA BUIDL (BLACKROCK)
    buidl_address = w3.to_checksum_address("0x7712c34205737192402172409a8f7ccef8aa2aec")
    buidl_abi = [
        {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
    ]
    
    contrato_buidl = w3.eth.contract(address=buidl_address, abi=buidl_abi)
    print("🏢 Extrayendo reservas institucionales de BUIDL...")
    
    decimales = contrato_buidl.functions.decimals().call()
    tokens_buidl = float(contrato_buidl.functions.totalSupply().call() / (10 ** decimales))
    valor_total_usd = tokens_buidl * 1.00  # Anclaje 1:1 con el dólar
    
    # 2. INYECCIÓN A LA BASE DE DATOS
    print("☁️  Inyectando reporte en Supabase...")
    try:
        respuesta = supabase.table('auditorias_buidl').insert({
            "tokens_buidl": tokens_buidl,
            "valor_total_usd": valor_total_usd
        }).execute()
        print("💾 ¡Inyección exitosa! Los datos de BlackRock están seguros en la nube.")
    except Exception as e:
        print(f"❌ Error al guardar en Supabase: {e}")
        
    print("-" * 55)
    print(f"🏦 VALOR INSTITUCIONAL REGISTRADO: ${valor_total_usd:,.2f} USD")
    print("-" * 55)
    
else:
    print("❌ Error de conexión al nodo RPC.")