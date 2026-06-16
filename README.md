# Juegos-Casino

Colección de scripts en Python que simulan los juegos de azar más populares de los casinos. Esta versión incluye simuladores de consola robustos y una nueva interfaz gráfica interactiva en 2D.

##  Juegos Implementados

### 1. Blackjack (`Blackjack/Blackjack.py`)
Un simulador de consola robusto que aplica reglas avanzadas de casino y gestión de capital.

**Características:**
- **Zapato Realista y Dinámico:** Utiliza 6 barajas (312 cartas) e implementa un sistema de re-mezclado dinámico (*shoe rebalancing*) que recrea el mazo automáticamente cuando resta menos del 15% de las cartas.
- **Reglas de Casino Puras:** Pago de Blackjack natural a 3:2. El *dealer* pide carta con un 17 suave y se planta con 17 duro (Regla H17).
- **Acciones Avanzadas del Jugador:** - Las acciones básicas: Pedir, Plantarse, Doblar (Double Down) y Dividir (Split).
  - **Seguro (Insurance):** Ofrece comprar seguro si la carta visible del dealer es un As.
  - **Rendición (Early Surrender):** Permite al jugador retirarse de la mano perdiendo solo la mitad de su apuesta inicial.

### 2. Ruleta (`Ruleta/`)
Incluye un simulador de consola detallado y una **nueva versión con Interfaz Gráfica de Usuario (GUI)**.

**Características:**
- **Versión GUI (`Ruleta_GUI.py`):** Desarrollada con Pygame y OpenGL. Cuenta con texturas generadas dinámicamente, animación de giro con frenado progresivo, un tablero de apuestas interactivo para Color/Paridad y un temporizador de 15 segundos para giros automáticos.
- **Versión Consola (`Ruleta.py`):** Soporta apuestas *Inside* (Straight Up, Split, Street, Corner, Line, Five Number) y apuestas *Outside* (Color, Par/Impar, Alto/Bajo, Docenas, Columnas) con pagos estadísticamente precisos.
- **Variantes Soportadas:** Ruleta Europea (un cero) y Ruleta Americana (doble cero) en ambas versiones.

### 3. Póker Texas Hold'em (`Poker/Poker_(Texas Hold'em).py`)
Módulo base para la simulación del Póker Texas Hold'em.

**Características actuales:**
- Generación y mezcla estocástica de baraja estándar de 52 cartas con palos y valores.
- Distribución de manos iniciales (Pre-Flop) para mesas configurables.
- Funciones preparadas para el reparto de cartas comunitarias (Flop, Turn, River).

##  Estructura de Directorios

- `Blackjack/`: Lógica algorítmica y juego en consola de Veintiuna.
- `Ruleta/`: Motor de pagos, interfaz de consola y versión gráfica interactiva (OpenGL).
- `Poker/`: Control de flujo para rondas de póker y simulaciones de cartas.

##  Requisitos y Ejecución

**Requisitos:**
Para jugar las versiones de consola solo necesitas Python 3.x. Para la Ruleta GUI, instala las siguientes dependencias:
```bash
pip install pygame PyOpenGL
```

##  Instrucciones de Ejecución:

Bash
# Para Blackjack:
python Blackjack/Blackjack.py

# Para Ruleta (Consola o GUI):
python Ruleta/Ruleta.py
python Ruleta/Ruleta_GUI.py

# Para Póker:
python "Poker/Poker_(Texas Hold'em).py"
