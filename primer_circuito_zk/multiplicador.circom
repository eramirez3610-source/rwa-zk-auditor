pragma circom 2.0.0;

// Definimos la plantilla (el molde) de nuestro circuito
template Multiplicador() {
    // 1. Declaración de Señales (Variables)
    signal input a;
    signal input b;
    signal output c;

    // 2. La Restricción Matemática (El corazón de ZK)
    c <== a * b;
}

// 3. Instanciamos el componente principal
component main = Multiplicador();