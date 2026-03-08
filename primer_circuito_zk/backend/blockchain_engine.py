import json
import os
import time
from web3 import Web3
from solcx import compile_standard, install_solc

class ZKEngine:
    """
    Motor de Blockchain para Auditoría RWA con Zero-Knowledge Proofs.
    Optimizado para evitar caché de compilación en despliegues locales.
    """
    def __init__(self, rpc_url="http://127.0.0.1:8545"):
        # Conexión al nodo local (Ganache)
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        # Instalación de solc compatible con Apple Silicon M4
        install_solc("0.8.0")

    def load_zk_proof(self):
        """Carga y formatea los datos de la prueba ZK."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        proof_path = os.path.normpath(os.path.join(base_path, '..', 'data', 'proof_solvencia.json'))
        public_path = os.path.normpath(os.path.join(base_path, '..', 'data', 'public_solvencia.json'))

        if not os.path.exists(proof_path) or not os.path.exists(public_path):
            raise FileNotFoundError("No se encontraron los archivos de la prueba en /data.")

        with open(proof_path, 'r') as f:
            p = json.load(f)
        with open(public_path, 'r') as f:
            pub = json.load(f)

        # Formateo para Groth16 (Solidity)
        a = [int(p['pi_a'][0]), int(p['pi_a'][1])]
        b = [
            [int(p['pi_b'][0][1]), int(p['pi_b'][0][0])], 
            [int(p['pi_b'][1][1]), int(p['pi_b'][1][0])]
        ]
        c = [int(p['pi_c'][0]), int(p['pi_c'][1])]
        inputs = [int(x) for x in pub]

        return a, b, c, inputs

    def generate_fake_proof(self):
        """Genera una prueba corrupta alterando un valor matemático."""
        a, b, c, inputs = self.load_zk_proof()
        # Alteramos 'a' para romper la paridad de la curva BN128
        corrupted_a = [a[0] + 1, a[1]]
        return corrupted_a, b, c, inputs

    def deploy_contract(self, file_path, contract_name, constructor_args=None):
        """
        Compila y despliega forzando una nueva versión cada vez para evitar caché,
        usando el nombre de archivo real para evitar KeyErrors.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo .sol no encontrado: {file_path}")

        contracts_dir = os.path.dirname(os.path.abspath(file_path))
        file_name = os.path.basename(file_path) # BovedaRWA.sol

        with open(file_path, "r") as f:
            source_code = f.read()

        # BYPASS DE CACHÉ: Añadimos un timestamp único al código
        source_code += f"\n// Update: {time.time()}"

        # Compilación estándar de Solidity
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {file_name: {"content": source_code}},
            "settings": {
                "outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}
            }
        }, 
        solc_version="0.8.0",
        base_path=contracts_dir,
        allow_paths=[contracts_dir]
        )

        # Extracción de Bytecode y ABI usando las llaves dinámicas correctas
        bytecode = compiled_sol["contracts"][file_name][contract_name]["evm"]["bytecode"]["object"]
        abi = compiled_sol["contracts"][file_name][contract_name]["abi"]

        deployer_account = self.w3.eth.accounts[0]
        ContractFactory = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        # Transacción de despliegue
        if constructor_args:
            tx_hash = ContractFactory.constructor(*constructor_args).transact({'from': deployer_account})
        else:
            tx_hash = ContractFactory.constructor().transact({'from': deployer_account})

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return self.w3.to_checksum_address(receipt.contractAddress), abi