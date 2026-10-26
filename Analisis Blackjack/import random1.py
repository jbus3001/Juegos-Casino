import random
import time

# --- CONFIGURACIÓN DEL SISTEMA ---
SIMULACIONES = 10000       # Límite máximo de iteraciones (seguridad)
CAPITAL_INICIAL = 10000    # C_0
META_OBJETIVO = 15000      # Barrera Superior (Take Profit)
APUESTA_BASE = 100         # Unidad de apuesta mínima
PAGO_BLACKJACK = 1.5       # 3:2

# Espacio Muestral (Cartas)
BARAJA = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALORES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def obtener_carta():
    return random.choice(BARAJA)

def calcular_mano(mano):
    total = 0
    ases = 0
    for carta in mano:
        valor = VALORES[carta]
        total += valor
        if carta == 'A':
            ases += 1
    
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
        
    es_suave = (ases > 0)
    return total, es_suave

def estrategia_basica(mano_jugador, carta_dealer):
    total, suave = calcular_mano(mano_jugador)
    upcard = VALORES[carta_dealer]
    
    # Pares (Simplificado)
    if len(mano_jugador) == 2 and mano_jugador[0] == mano_jugador[1]:
        carta = mano_jugador[0]
        if carta in ['A', '8']: return 'SP' 

    puede_doblar = (len(mano_jugador) == 2)

    if suave:
        if total >= 19: return 'Q'
        if total == 18:
            if upcard in [2, 3, 4, 5, 6]: return 'D' if puede_doblar else 'Q'
            if upcard in [9, 10, 11]: return 'P'
            return 'Q'
        if total == 17:
            return 'D' if (puede_doblar and upcard in [3, 4, 5, 6]) else 'P'
        if total in [15, 16]:
            return 'D' if (puede_doblar and upcard in [4, 5, 6]) else 'P'
        if total in [13, 14]:
            return 'D' if (puede_doblar and upcard in [5, 6]) else 'P'
        return 'P'
    else:
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

def jugar_mano(capital_actual, numero_juego):
    puede_pagar_doble = capital_actual >= (APUESTA_BASE * 2)
    
    mano_jugador = [obtener_carta(), obtener_carta()]
    mano_dealer = [obtener_carta(), obtener_carta()]
    
    apuesta = APUESTA_BASE
    acciones_str = ""
    
    val_j, _ = calcular_mano(mano_jugador)
    val_d, _ = calcular_mano(mano_dealer)
    
    resultado_str = ""
    delta_capital = 0

    # 1. Check BJ Natural
    if val_j == 21:
        if val_d == 21:
            resultado_str = "EMPATE (BJ)"
            delta_capital = 0
        else:
            resultado_str = "VICTORIA (BJ)"
            delta_capital = apuesta * PAGO_BLACKJACK
        imprimir_linea(numero_juego, mano_jugador, val_j, mano_dealer, val_d, "BJ Nat", resultado_str, capital_actual + delta_capital)
        return capital_actual + delta_capital, 1 if delta_capital > 0 else 0, 0, 1 if delta_capital == 0 else 0

    # 2. Turno Jugador
    while True:
        val_j, _ = calcular_mano(mano_jugador)
        if val_j > 21:
            resultado_str = "DERROTA (Bust)"
            delta_capital = -apuesta
            imprimir_linea(numero_juego, mano_jugador, val_j, mano_dealer, val_d, acciones_str, resultado_str, capital_actual + delta_capital)
            return capital_actual + delta_capital, 0, 1, 0
        
        accion = estrategia_basica(mano_jugador, mano_dealer[0])
        if accion == 'SP': accion = 'P'

        if accion == 'D' and not puede_pagar_doble:
            accion = 'P'

        if accion == 'Q':
            acciones_str += "Stand "
            break
        elif accion == 'P':
            acciones_str += "Hit "
            mano_jugador.append(obtener_carta())
        elif accion == 'D':
            acciones_str += "Dbl "
            apuesta *= 2
            mano_jugador.append(obtener_carta())
            val_j, _ = calcular_mano(mano_jugador)
            if val_j > 21:
                resultado_str = "DERROTA (Dbl Bust)"
                delta_capital = -apuesta
                imprimir_linea(numero_juego, mano_jugador, val_j, mano_dealer, val_d, acciones_str, resultado_str, capital_actual + delta_capital)
                return capital_actual + delta_capital, 0, 1, 0
            break

    # 3. Turno Dealer
    while True:
        val_d, _ = calcular_mano(mano_dealer)
        if val_d >= 17: break
        mano_dealer.append(obtener_carta())

    # 4. Resolución
    val_j, _ = calcular_mano(mano_jugador)
    val_d, _ = calcular_mano(mano_dealer)

    if val_d > 21:
        resultado_str = "VICTORIA (Dlr Bust)"
        delta_capital = apuesta
    elif val_j > val_d:
        resultado_str = "VICTORIA (Puntos)"
        delta_capital = apuesta
    elif val_j < val_d:
        resultado_str = "DERROTA (Puntos)"
        delta_capital = -apuesta
    else:
        resultado_str = "EMPATE"
        delta_capital = 0

    nuevo_capital = capital_actual + delta_capital
    imprimir_linea(numero_juego, mano_jugador, val_j, mano_dealer, val_d, acciones_str, resultado_str, nuevo_capital)
    
    g = 1 if delta_capital > 0 else 0
    p = 1 if delta_capital < 0 else 0
    e = 1 if delta_capital == 0 else 0
    return nuevo_capital, g, p, e

def imprimir_linea(n, m_jug, v_jug, m_dlr, v_dlr, acc, res, cap):
    s_jug = f"{str(m_jug)}={v_jug}"
    s_dlr = f"{str(m_dlr)}={v_dlr}"
    print(f"| {n:<5} | {s_jug:<22} | {s_dlr:<22} | {acc:<12} | {res:<20} | {cap:>8.1f} |")

# --- MOTOR PRINCIPAL ---

print("="*105)
print(f"| {'N':<5} | {'JUGADOR (Cartas=Suma)':<22} | {'DEALER (Cartas=Suma)':<22} | {'ACCIONES':<12} | {'RESULTADO':<20} | {'CAPITAL':>8} |")
print("="*105)

capital = CAPITAL_INICIAL
stats_g = 0
stats_p = 0
stats_e = 0
manos_jugadas = 0
causa_fin = "Límite de Simulaciones" # Por defecto

for i in range(SIMULACIONES):
    # --- CONDICIONES DE FRONTERA ---
    
    # 1. Barrera Absorbente Inferior (Ruina)
    if capital < APUESTA_BASE:
        causa_fin = "RUINA DEL JUGADOR (Capital Insuficiente)"
        break
    
    # 2. Barrera Absorbente Superior (Objetivo Alcanzado)
    if capital >= META_OBJETIVO:
        causa_fin = "META ALCANZADA (Take Profit)"
        break

    capital, g, p, e = jugar_mano(capital, i + 1)
    stats_g += g
    stats_p += p
    stats_e += e
    manos_jugadas += 1

# --- ANÁLISIS POST-MORTEM ---
print("="*105)
if manos_jugadas == 0:
    print(f"La simulación no comenzó. Revisa el capital inicial vs meta.")
else:
    print(f"SIMULACIÓN DETENIDA EN LA MANO {manos_jugadas}")
    print(f"CAUSA: {causa_fin}")
    print("-" * 40)
    print(f"Capital Inicial: {CAPITAL_INICIAL}")
    print(f"Capital Final:   {capital}")
    print(f"Meta Objetivo:   {META_OBJETIVO}")
    
    delta = capital - CAPITAL_INICIAL
    roi = (delta / CAPITAL_INICIAL) * 100
    
    print(f"Balance Neto:    {delta} ({roi:.2f}% ROI)")
    print("-" * 40)
    print(f"Victorias: {stats_g} ({stats_g/manos_jugadas*100:.1f}%)")
    print(f"Derrotas:  {stats_p} ({stats_p/manos_jugadas*100:.1f}%)")
    print(f"Empates:   {stats_e} ({stats_e/manos_jugadas*100:.1f}%)")
print("="*105)