import random
import matplotlib.pyplot as plt
from collections import Counter

# --- CONFIGURACIÓN DEL SISTEMA ---
SIMULACIONES = 10000       
CAPITAL_INICIAL = 10000    
META_OBJETIVO = 15000      
APUESTA_BASE = 100         
PAGO_BLACKJACK = 1.5       

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
        if carta == 'A': ases += 1
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    return total, (ases > 0)

def estrategia_basica(mano_jugador, carta_dealer):
    total, suave = calcular_mano(mano_jugador)
    upcard = VALORES[carta_dealer]
    if len(mano_jugador) == 2 and mano_jugador[0] == mano_jugador[1]:
        if mano_jugador[0] in ['A', '8']: return 'SP' 
    puede_doblar = (len(mano_jugador) == 2)
    if suave:
        if total >= 19: return 'Q'
        if total == 18:
            if upcard in [2, 3, 4, 5, 6]: return 'D' if puede_doblar else 'Q'
            if upcard in [9, 10, 11]: return 'P'
            return 'Q'
        if total == 17: return 'D' if (puede_doblar and upcard in [3, 4, 5, 6]) else 'P'
        if total in [15, 16]: return 'D' if (puede_doblar and upcard in [4, 5, 6]) else 'P'
        if total in [13, 14]: return 'D' if (puede_doblar and upcard in [5, 6]) else 'P'
        return 'P'
    else:
        if total >= 17: return 'Q'
        if total in [13, 14, 15, 16]: return 'Q' if upcard in [2, 3, 4, 5, 6] else 'P'
        if total == 12: return 'Q' if upcard in [4, 5, 6] else 'P'
        if total == 11: return 'D' if puede_doblar else 'P'
        if total == 10: return 'D' if (puede_doblar and upcard < 10) else 'P'
        if total == 9: return 'D' if (puede_doblar and upcard in [3, 4, 5, 6]) else 'P'
        return 'P'

def jugar_mano(capital_actual):
    puede_pagar_doble = capital_actual >= (APUESTA_BASE * 2)
    
    # Registro de la mano inicial (ordenada para consistencia estadística)
    mano_jugador = sorted([obtener_carta(), obtener_carta()], key=lambda x: str(VALORES[x]))
    mano_str = f"{mano_jugador[0]}-{mano_jugador[1]}"
    
    mano_dealer = [obtener_carta(), obtener_carta()]
    apuesta = APUESTA_BASE
    
    val_j, _ = calcular_mano(mano_jugador)
    val_d, _ = calcular_mano(mano_dealer)
    
    if val_j == 21:
        delta = 0 if val_d == 21 else apuesta * PAGO_BLACKJACK
        return capital_actual + delta, 1 if delta > 0 else 0, 0, 1 if delta == 0 else 0, mano_str

    while True:
        val_j, _ = calcular_mano(mano_jugador)
        if val_j > 21: return capital_actual - apuesta, 0, 1, 0, mano_str
        accion = estrategia_basica(mano_jugador, mano_dealer[0])
        if accion == 'SP' or accion == 'Q': break
        elif accion == 'P': mano_jugador.append(obtener_carta())
        elif accion == 'D':
            apuesta *= 2
            mano_jugador.append(obtener_carta())
            val_j, _ = calcular_mano(mano_jugador)
            if val_j > 21: return capital_actual - apuesta, 0, 1, 0, mano_str
            break

    while True:
        val_d, _ = calcular_mano(mano_dealer)
        if val_d >= 17: break
        mano_dealer.append(obtener_carta())

    val_j, _ = calcular_mano(mano_jugador)
    val_d, _ = calcular_mano(mano_dealer)
    if val_d > 21 or val_j > val_d: delta = apuesta
    elif val_j < val_d: delta = -apuesta
    else: delta = 0
    return capital_actual + delta, 1 if delta > 0 else 0, 1 if delta < 0 else 0, 1 if delta == 0 else 0, mano_str

# --- MOTOR DE SIMULACIÓN ---

capital = CAPITAL_INICIAL
historial_capital = [CAPITAL_INICIAL]
frecuencia_manos = []
stats = {'V': 0, 'D': 0, 'E': 0}

for i in range(1, SIMULACIONES + 1):
    if capital < APUESTA_BASE or capital >= META_OBJETIVO: break

    capital, v, d, e, mano_inicial = jugar_mano(capital)
    stats['V'] += v
    stats['D'] += d
    stats['E'] += e
    historial_capital.append(capital)
    frecuencia_manos.append(mano_inicial)

# --- VISUALIZACIÓN ---

# Contabilizar las 15 manos más frecuentes
conteo_manos = Counter(frecuencia_manos).most_common(15)
manos_labels, manos_counts = zip(*conteo_manos)

plt.figure(figsize=(15, 10))

# 1. Trayectoria de Capital
plt.subplot(2, 2, 1)
plt.plot(historial_capital, color='#1f77b4')
plt.axhline(y=META_OBJETIVO, color='g', linestyle='--')
plt.title('Trayectoria Estocástica del Capital')
plt.grid(alpha=0.3)

# 2. Balance de Resultados
plt.subplot(2, 2, 2)
plt.pie([stats['V'], stats['D'], stats['E']], labels=['Victorias', 'Derrotas', 'Empates'], 
        autopct='%1.1f%%', colors=['#2ca02c', '#d62728', '#7f7f7f'], startangle=140)
plt.title('Distribución de Resultados Finales')

# 3. Frecuencia de Manos Iniciales (Distribución Empírica)
plt.subplot(2, 1, 2)
plt.bar(manos_labels, manos_counts, color='#9467bd')
plt.title('Top 15: Frecuencia de Manos Iniciales Obtenidas')
plt.ylabel('Cantidad de veces')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()