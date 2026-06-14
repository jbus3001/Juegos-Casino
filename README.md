# Juegos-Casino

Colección de scripts en Python que simulan los juegos de azar más populares de los casinos, comenzando con una implementación completa y orientada a la probabilidad del Blackjack (Veintiuna).

##  Juegos Implementados

### 1. Blackjack (`Blackjack.py`)
Un simulador de consola robusto que aplica las reglas estándar de casino y gestión de capital.

**Características:**
- **Zapato Realista:** Utiliza 6 barajas (312 cartas) con punto de penetración; se baraja automáticamente cuando restan 70 cartas o menos.
- **Gestión de Bankroll:** Sistema de apuestas con validación de liquidez. El jugador comienza con un capital de $1000 y apuestas permitidas entre $10 y $500.
- **Reglas de Casino Puras:** - Pago de Blackjack natural a 3:2.
  - El *dealer* debe pedir carta con un 17 suave y plantarse con 17 duro (Regla H17).
  - Colapso dinámico del valor del As (11 a 1) al exceder los 21 puntos.
- **Acciones del Jugador:**
  - **Pedir / Plantarse:** Flujo continuo hasta alcanzar límite o decisión.
  - **Doblar (Double Down):** Permite duplicar la apuesta a cambio de una sola carta adicional (requiere fondos suficientes).
  - **Dividir (Split):** Permite separar pares iniciales en dos manos independientes jugadas secuencialmente.

##  Estructura del Código

- `Blackjack.py`: Archivo principal de ejecución. Contiene el bucle del juego (Game Loop), la interfaz de terminal y la gestión de estado del jugador (capital, apuestas, selección de acciones).
- `Funciones_Casino.py`: Módulo de lógica estocástica. Contiene el motor de cálculo de manos, la evaluación de condiciones de victoria, el autómata del *dealer* y la administración del mazo mediante la librería `random`.

##  Requisitos y Ejecución

**Requisitos:**
- Python 3.x (No requiere librerías externas más allá de las estándar `random` y `time`).

**Instrucciones:**
Para iniciar una sesión de juego, ejecuta en tu terminal:
```bash
python Blackjack.py
