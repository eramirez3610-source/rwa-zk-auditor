pragma circom 2.0.0;

// Importamos el comparador y el algoritmo Poseidon desde el arsenal
include "node_modules/circomlib/circuits/comparators.circom";
include "node_modules/circomlib/circuits/poseidon.circom";

template PruebaDeSolvencia() {
    // 🕵️‍♂️ ENTRADAS PRIVADAS (Solo tu Mac verá esto)
    signal input saldo;
    signal input secreto_id; // Un "PIN" aleatorio para que nadie adivine tu hash

    // 📢 ENTRADA PÚBLICA (El requisito del banco, ej. "Mayor a 0" o "Mayor a 1000")
    signal input limite_minimo;

    // 🎯 SALIDA PÚBLICA (El hash que Solidity buscará en el Árbol de Merkle)
    signal output hash_hoja;

    // --- RESTRICCIÓN 1: ¿Es el saldo mayor o igual al límite? ---
    // Usamos un comparador de 64 bits (soporta números gigantes)
    component comparador = GreaterEqThan(64); 
    comparador.in[0] <== saldo;
    comparador.in[1] <== limite_minimo;
    
    // Obligamos a que el resultado sea 1 (Verdadero). Si no, la prueba explota.
    comparador.out === 1; 

    // --- RESTRICCIÓN 2: Generar la huella digital (Hash Poseidon) ---
    component hasher = Poseidon(2);
    hasher.inputs[0] <== saldo;
    hasher.inputs[1] <== secreto_id;
    
    // Escupimos el hash hacia el mundo exterior
    hash_hoja <== hasher.out;
}

// Declaramos que el límite mínimo es la única variable que el mundo podrá ver
component main {public [limite_minimo]} = PruebaDeSolvencia();