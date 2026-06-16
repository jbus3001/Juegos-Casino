# Juegos-Casino

Colección de scripts en Python que simulan los juegos de azar más populares de los casinos.

##  Juegos Implementados

### 1. Blackjack (`Blackjack/Blackjack.py`)
Un simulador de consola robusto que aplica las reglas estándar de casino y gestión de capital.

**Características:**
- **Zapato Realista:** Utiliza 6 barajas (312 cartas) con punto de penetración; se baraja automáticamente cuando restan 70 cartas o menos.
- **Gestión de Bankroll:** Sistema de apuestas con validación de liquidez. El jugador comienza con un capital de $1000 y apuestas permitidas entre $10 y $500.
- **Reglas de Casino Puras:** Pago de Blackjack natural a 3:2. El *dealer* debe pedir carta con un 17 suave y plantarse con 17 duro (Regla H17).
- **Acciones del Jugador:** Pedir, Plantarse, Doblar (Double Down) y Dividir (Split).

### 2. Ruleta (`Ruleta/Ruleta.py`)
Simulador interactivo que permite jugar en las dos variantes principales de ruleta del mundo.

**Características:**
- **Variantes Soportadas:** Ruleta Europea (un cero) y Ruleta Americana (doble cero) con sus respectivas distribuciones de colores y pagos.
- **Tipos de Apuesta:** Soporta apuestas *Inside* (Straight Up, Split, Street, Corner, Line, Five Number) y apuestas *Outside* (Color, Par/Impar, Alto/Bajo, Docenas, Columnas).
- **Motor de Pagos:** Cálculo automático de ganancias basado en multiplicadores reales de casino según el tipo de apuesta y el monto ingresado.

### 3. Póker Texas Hold'em (`Poker/Poker_(Texas Hold'em).py`)
Módulo base para la simulación del Póker Texas Hold'em.

**Características actuales:**
- Generación y mezcla estocástica de baraja estándar de 52 cartas con palos y valores estructurados.
- Distribución de manos iniciales (Pre-Flop) para mesas configurables (actualmente programado para 5 jugadores).
- Infraestructura preparada para el manejo de cartas comunitarias (Flop, Turn, River).

##  Estructura del Código

- `Blackjack/Blackjack.py` / `Blackjack/Funciones_Blackjack.py`: Lógica de presentación y evaluación del juego de Blackjack.
- `Ruleta/Ruleta.py` / `Ruleta/Funciones_Ruleta.py`: Bucle interactivo de apuestas y diccionarios de evaluación probabilística de la mesa de ruleta.
- `Poker/Poker_(Texas Hold'em).py` / `Poker/Funciones_Poker.py`: Control de flujo para rondas de póker y manejo del estado de la baraja.

##  Requisitos y Ejecución

**Requisitos:**
- Python 3.x (No requiere librerías externas; utiliza `random` y `time`).

**Instrucciones:**
Para iniciar un juego, ejecuta en terminal el archivo principal correspondiente:
```bash
python Blackjack/Blackjack.py
python Ruleta/Ruleta.py
python "Poker/Poker_(Texas Hold'em).py"
