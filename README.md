# 🏦 ZK-Proof of Reserves (Prueba de Reservas Institucional)

Este repositorio contiene una arquitectura híbrida de prueba de concepto para auditar pasivos bancarios utilizando criptografía tradicional y Pruebas de Conocimiento Cero (Zero-Knowledge Proofs).

## 🎯 Objetivo del Proyecto
Demostrar cómo una institución financiera puede probar matemáticamente on-chain que posee fondos suficientes para cubrir los saldos de sus clientes, permitiendo a clientes específicos (VIP/ZK) validar su solvencia en un entorno Web3 sin revelar su saldo real ni su identidad al público.

## 🛠️ Tecnologías Utilizadas
* **Python & Web3.py:** Construcción del Árbol de Merkle off-chain integrando el estándar Keccak-256.
* **Circom & SnarkJS:** Desarrollo de circuitos ZK (Groth16) y generación de pruebas matemáticas usando el algoritmo de hasheo de grado militar Poseidon.
* **Solidity:** Contrato inteligente auditor que utiliza la librería `MerkleProof` de OpenZeppelin.
* **Ethereum (Remix VM):** Entorno de ejecución y validación on-chain.

## ⚙️ Arquitectura de la Operación
1. **El Motor ZK (Cliente Privado):** Un circuito en Circom verifica que el saldo de un usuario en la bóveda cumple con un límite mínimo requerido (ej. > $1,000 USD). Genera un Hash Poseidon único e irrepetible, comprobando la solvencia sin revelar el saldo real de la cuenta.
2. **El Banco Híbrido (TradFi + Web3):** Un script en Python construye un Árbol de Merkle combinando clientes tradicionales (saldos transparentes) con el comprobante ZK (Hash Poseidon) del cliente privado, generando una Raíz de Merkle criptográficamente inquebrantable.
3. **El Auditor Insobornable (Smart Contract):** Un contrato en Solidity almacena la Raíz de Merkle pública. Cualquier usuario puede enviar su prueba criptográfica al contrato para verificar de forma descentralizada si sus fondos están matemáticamente respaldados por las reservas del banco.