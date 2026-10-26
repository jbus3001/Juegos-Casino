import random

# --- CONFIGURACIÓN INICIAL ---
SIMULACIONES = 10000
CAPITAL_INICIAL = 10000
APUESTA_BASE = 100
PAGO_BLACKJACK = 1.5  # 3 a 2

# Valores de cartas
BARAJA = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALORES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def obtener_carta():
    """Retorna una carta aleatoria del mazo (Mazo infinito/Barajado continuo)"""
    return random.choice(BARAJA)

def calcular_mano(mano):
    """
    Calcula el valor de la mano y determina si es 'suave' (tiene As utilizable como 11).
    Retorna: (total, es_suave)
    """
    total = 0
    ases = 0
    for carta in mano:
        valor = VALORES[carta]
        total += valor
        if carta == 'A':
            ases += 1
    
    # Ajuste de Ases si nos pasamos de 21
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
        
    # Es suave si tenemos un As que todavía cuenta como 11
    # (Si ases > 0 despues del ajuste, significa que queda al menos un As valiendo 11)
    es_suave = (ases > 0)
    return total, es_suave

def estrategia_basica(mano_jugador, carta_dealer):
    """
    Implementación del Algoritmo de Decisión Óptima (Estrategia Básica).
    Retorna: 'P' (Pedir), 'Q' (Quedarse/Plantarse), 'D' (Doblar), 'SP' (Dividir)
    """
    total, suave = calcular_mano(mano_jugador)
    upcard = VALORES[carta_dealer]
    
    # 1. PARES (Simplificación: Solo dividimos Ases y Ochos para mantener el código lineal)
    # En una simulación completa, dividir crea sub-juegos. Aquí, si no es A u 8, jugamos la suma.
    if len(mano_jugador) == 2 and mano_jugador[0] == mano_jugador[1]:
        carta = mano_jugador[0]
        if carta in ['A', '8']:
            return 'SP' # Split (En esta sim simplificada, Split de Ases/8s se tratará como 'Pedir' agresivo para no romper el flujo lineal)

    # Lógica de juego (Si decidimos doblar pero tenemos más de 2 cartas, solo pedimos)
    puede_doblar = (len(mano_jugador) == 2)

    if suave:
        # MANOS SUAVES (A + X)
        if total >= 19: return 'Q'
        if total == 18:
            if upcard in [2, 3, 4, 5, 6]: return 'D' if puede_doblar else 'Q' # Doblar o Quedarse (pequeña corrección a pedir si no se puede doblar no aplica aqui)
            if upcard in [9, 10, 11]: return 'P'
            return 'Q' # Contra 7 u 8
        if total == 17:
            return 'D' if (puede_doblar and upcard in [3, 4, 5, 6]) else 'P'
        if total in [15, 16]:
            return 'D' if (puede_doblar and upcard in [4, 5, 6]) else 'P'
        if total in [13, 14]:
            return 'D' if (puede_doblar and upcard in [5, 6]) else 'P'
        return 'P' # 12 suave o menos

    else:
        # MANOS DURAS
        if total >= 17: return 'Q'
        if total in [13, 14, 15, 16]:
            if upcard in [2, 3, 4, 5, 6]: return 'Q'
            return 'P'
        if total == 12:
            if upcard in [4, 5, 6]: return 'Q'
            return 'P'
        if total == 11: return 'D' if puede_doblar else 'P'
        if total == 10: return 'D' if (puede_doblar and upcard < 10) else 'P'
        if total == 9: return 'D' if (puede_doblar and upcard in [3, 4, 5, 6]) else 'P'
        return 'P'

def jugar_mano(capital_actual):
    mano_jugador = [obtener_carta(), obtener_carta()]
    mano_dealer = [obtener_carta(), obtener_carta()]
    
    apuesta = APUESTA_BASE
    acciones_log = []
    
    # 1. Verificar Blackjack Natural
    val_j, suave_j = calcular_mano(mano_jugador)
    val_d, _ = calcular_mano(mano_dealer)
    
    if val_j == 21:
        if val_d == 21:
            return capital_actual, "EMPATE (BJ vs BJ)", mano_jugador, mano_dealer, "BJ"
        else:
            return capital_actual + (apuesta * PAGO_BLACKJACK), "VICTORIA (BJ)", mano_jugador, mano_dealer, "BJ"

    # 2. Turno del Jugador
    while True:
        val_j, suave_j = calcular_mano(mano_jugador)
        if val_j > 21:
            return capital_actual - apuesta, "DERROTA (Bust)", mano_jugador, mano_dealer, acciones_log
        
        accion = estrategia_basica(mano_jugador, mano_dealer[0])
        
        # Simplificación de Split para flujo lineal: Si sale Split (SP), lo tratamos como una mano fuerte y Pedimos
        # En una simulación de Montecarlo rigurosa, esto debería bifurcar el objeto juego.
        if accion == 'SP': accion = 'P' 

        if accion == 'Q':
            acciones_log.append('Stand')
            break
        elif accion == 'P':
            acciones_log.append('Hit')
            mano_jugador.append(obtener_carta())
        elif accion == 'D':
            acciones_log.append('Double')
            apuesta *= 2
            mano_jugador.append(obtener_carta())
            # Al doblar, se termina el turno forzosamente
            val_j, _ = calcular_mano(mano_jugador)
            if val_j > 21:
                return capital_actual - apuesta, "DERROTA (Double Bust)", mano_jugador, mano_dealer, acciones_log
            break

    # 3. Turno del Dealer (Algoritmo determinista)
    # Regla: Dealer pide con 16 o menos. Se planta con 17 o más.
    while True:
        val_d, _ = calcular_mano(mano_dealer)
        if val_d >= 17:
            break
        mano_dealer.append(obtener_carta())

    # 4. Resolución
    val_j, _ = calcular_mano(mano_jugador) # Recalcular final
    val_d, _ = calcular_mano(mano_dealer)

    if val_d > 21:
        return capital_actual + apuesta, "VICTORIA (Dealer Bust)", mano_jugador, mano_dealer, acciones_log
    elif val_j > val_d:
        return capital_actual + apuesta, "VICTORIA (Puntos)", mano_jugador, mano_dealer, acciones_log
    elif val_j < val_d:
        return capital_actual - apuesta, "DERROTA (Puntos)", mano_jugador, mano_dealer, acciones_log
    else:
        return capital_actual, "EMPATE", mano_jugador, mano_dealer, acciones_log

# --- EJECUCIÓN DE LA SIMULACIÓN ---
historial = []
capital = CAPITAL_INICIAL
victorias = 0
empates = 0
derrotas = 0

print(f"Iniciando simulación de {SIMULACIONES} manos...")
print(f"Capital Inicial: {CAPITAL_INICIAL}")
print("-" * 60)

for i in range(SIMULACIONES):
    capital_previo = capital
    capital, resultado, mano_j, mano_d, acciones = jugar_mano(capital)
    
    # Registro de estadísticas
    if capital > capital_previo: victorias += 1
    elif capital < capital_previo: derrotas += 1
    else: empates += 1
    
    # Guardar en historial
    registro = {
        "N": i + 1,
        "Jugador": f"{mano_j} ({calcular_mano(mano_j)[0]})",
        "Dealer": f"{mano_d} ({calcular_mano(mano_d)[0]})",
        "Estrategia": acciones,
        "Resultado": resultado,
        "Capital": capital
    }
    historial.append(registro)

# --- REPORTE DE RESULTADOS ---

# Mostrar las primeras 5 jugadas
print("\n--- PRIMERAS 5 JUGADAS ---")
for h in historial[:5]:
    print(f"#{h['N']} | J: {h['Jugador']} vs D: {h['Dealer']} | Acc: {h['Estrategia']} | {h['Resultado']} | Cap: {h['Capital']}")

# Mostrar las últimas 5 jugadas
print("\n--- ÚLTIMAS 5 JUGADAS ---")
for h in historial[-5:]:
    print(f"#{h['N']} | J: {h['Jugador']} vs D: {h['Dealer']} | Acc: {h['Estrategia']} | {h['Resultado']} | Cap: {h['Capital']}")

# Análisis Final
print("\n" + "="*30)
print("ESTADÍSTICAS FINALES")
print("="*30)
print(f"Total Manos: {SIMULACIONES}")
print(f"Capital Final: {capital}")
print(f"Retorno Neto: {capital - CAPITAL_INICIAL}")
print(f"Victorias: {victorias} ({victorias/SIMULACIONES*100:.2f}%)")
print(f"Derrotas:  {derrotas} ({derrotas/SIMULACIONES*100:.2f}%)")
print(f"Empates:   {empates} ({empates/SIMULACIONES*100:.2f}%)")

roi = ((capital - CAPITAL_INICIAL) / CAPITAL_INICIAL) * 100
print(f"ROI (Retorno de Inversión): {roi:.2f}%")
print("="*30)

if capital < CAPITAL_INICIAL:
    print("CONCLUSIÓN: Como predice la teoría, la ventaja de la casa (House Edge)")
    print("ha erosionado el capital a pesar de usar la estrategia óptima.")
else:
    print("CONCLUSIÓN: Has terminado positivo debido a la varianza a corto plazo,")
    print("pero recuerda que la esperanza matemática sigue siendo negativa a largo plazo.")