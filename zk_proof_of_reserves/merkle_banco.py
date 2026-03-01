from web3 import Web3

def crear_hash_keccak(texto):
    """Genera un hash Keccak-256 nativo de Ethereum."""
    return Web3.keccak(text=texto)

def emparejar_y_hashear(hash1, hash2):
    """Ordena y combina hashes al estándar de OpenZeppelin."""
    if hash1 < hash2:
        return Web3.keccak(hash1 + hash2)
    else:
        return Web3.keccak(hash2 + hash1)

# 1. LA BASE DE DATOS HÍBRIDA (Tradicional + ZK)
# Los primeros 3 usuarios son tradicionales
clientes_tradicionales = [
    {"id": "user_001", "saldo": 50000},
    {"id": "user_002", "saldo": 15000},
    {"id": "user_003", "saldo": 35000}
]

# 🕵️‍♂️ EL USUARIO ZK (Tú)
# El banco NO sabe tu saldo, solo tiene tu comprobante Poseidon
hash_poseidon_user_004 = "2391214763992426519047452138427810456362375813945847329134262877570034119538" 

print("🏦 INICIANDO AUDITORÍA INSTITUCIONAL (HÍBRIDA TRADFI + ZK) 🏦\n")

hojas = []

# Hasheamos a los clientes tradicionales
for cliente in clientes_tradicionales:
    datos = f"{cliente['id']}_{cliente['saldo']}"
    hojas.append(crear_hash_keccak(datos))

# Añadimos tu comprobante ZK al Árbol de Merkle
# Lo pasamos por Keccak para estandarizarlo con el resto del árbol
hojas.append(crear_hash_keccak(hash_poseidon_user_004))

# Construimos las ramas
rama_izquierda = emparejar_y_hashear(hojas[0], hojas[1])
rama_derecha = emparejar_y_hashear(hojas[2], hojas[3])

# La Raíz Definitiva
merkle_root = emparejar_y_hashear(rama_izquierda, rama_derecha)

print("🎯 MERKLE ROOT DEFINITIVA (Lista para el Smart Contract):")
print("0x" + merkle_root.hex())
print("\n¡El banco ha incluido tu solvencia sin conocer tu saldo real!")