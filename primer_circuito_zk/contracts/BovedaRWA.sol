// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title BovedaRWA
 * @dev Protocolo de Privacidad para Activos del Mundo Real (RWA) 
 * utilizando Zero-Knowledge Proofs (Groth16).
 */

// Importamos la interfaz del Verificador generado por Circom/SnarkJS
import "./Verifier.sol";

contract BovedaRWA {
    // Instancia del contrato verificador Groth16
    Groth16Verifier public verifier;

    // Mapping para registrar qué instituciones han pasado la auditoría
    mapping(address => bool) public isAudited;

    // EVENTO: Crucial para que el frontend (Streamlit) y Subgraphs detecten el éxito
    event AuditCompleted(address indexed institution, bool success);

    /**
     * @dev Constructor que enlaza la Bóveda con el Verificador ZK.
     * @param _verifierAddress Dirección del contrato Verifier.sol desplegado.
     */
    constructor(address _verifierAddress) {
        verifier = Groth16Verifier(_verifierAddress);
    }

    /**
     * @dev Valida la solvencia de una institución sin revelar su balance real.
     * @param a Punto A de la prueba Groth16.
     * @param b Puntos B de la prueba Groth16 (Matriz 2x2).
     * @param c Punto C de la prueba Groth16.
     * @param input Señales públicas (ej. el umbral de solvencia).
     */
    function validateIdentity(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[2] memory input
    ) public {
        // 1. Ejecutar la verificación matemática en la curva BN128
        bool isValid = verifier.verifyProof(a, b, c, input);
        
        // 2. REGLA DE ORO: Si la matemática no cuadra, la transacción se revierte.
        // Esto es lo que detiene el "Security Stress Test" con éxito.
        require(isValid, "Invalid ZK-Proof: Mathematical inconsistency detected");

        // 3. Si es válida, actualizamos el estado en la blockchain
        isAudited[msg.sender] = true;

        // 4. Emitimos el evento para confirmación off-chain
        emit AuditCompleted(msg.sender, true);
    }

    /**
     * @dev Función de lectura para consultar el estado de auditoría.
     */
    function checkAuditStatus(address _institution) public view returns (bool) {
        return isAudited[_institution];
    }
}