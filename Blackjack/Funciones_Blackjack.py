import random
import time

# Configuración del juego
APUESTA_MIN = 10
APUESTA_MAX = 500
RE_SPLIT_MAX = 3  # máximo 3 re‑splits → 4 manos simultáneas

#Preparamos un mazo de 6 barajas (312 cartas)
tipos_cartas = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
mazo = tipos_cartas * 24

valores_baraja = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

#Funcion para barajear las cartas
def preparar_mesa():
    tiempo_actual = time.time()
    random.seed(tiempo_actual) 
    random.shuffle(mazo)

#Funcion para crear un nuevo mazo de cartas (6 barajas) y barajearlo.
def nuevo_mazo():
    global mazo
    mazo = tipos_cartas * 24
    preparar_mesa()
    return mazo

#Funcion para obtener una carta del mazo.
#   de tener un numero menor o igual a 70, vuelve a hacer un nuevo mazo y barajearlo.
def obtener_carta():
    if len(mazo) <= 70:
        nuevo_mazo()
        preparar_mesa()
        return mazo.pop()
    return mazo.pop() 

#Funcion para repartir manos
def repartir_manos_inicio():
    mano_jugador = [obtener_carta(), obtener_carta()]
    mano_dealer = [obtener_carta(), obtener_carta()]
    return mano_jugador, mano_dealer

#Funcion para dar carta adicional a jugador
def dar_carta_jugador(mano_jugador):
    mano_jugador.append(obtener_carta())
    return mano_jugador

#Funcion para dar carta adicional a dealer
def dar_carta_dealer(mano_dealer):
    mano_dealer.append(obtener_carta())
    return mano_dealer

#calculamos el valor de la mano.
def calcular_mano(mano):
    total = 0
    ases = 0
    for carta in mano:
        valor = valores_baraja[carta]
        total += valor
        if carta == 'A': ases += 1
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1   
    return total, (ases > 0)

#Evaluamos las cartas del dealer 
def evaluacion_mano_dealer(mano_dealer):
    while True:
        valor, suave = calcular_mano(mano_dealer)
        if valor < 17 or (valor == 17 and suave):
            mano_dealer.append(obtener_carta())
        else:
            break
    return mano_dealer

#Acciones jugador
def plantarse(jugador, dealer, apuesta_base, capital, dealer_final=None, skip_dealer=False):
    print("Has decidido plantarte.")
    if not skip_dealer:
        print('La mano del dealer es: ')
        dealer_final = evaluacion_mano_dealer(dealer)
        print(dealer_final)
    else:
        dealer_final = dealer  
    val_jugador = calcular_mano(jugador)[0]
    val_dealer = calcular_mano(dealer_final)[0]
    if val_dealer > 21 or val_jugador > val_dealer:
        print("¡Has ganado!")
        capital += apuesta_base
        print(f"Tu capital actual es: ${capital}")
    elif val_jugador < val_dealer:
        print("Has perdido.")
        capital -= apuesta_base
        print(f"Tu capital actual es: ${capital}")
    else:
        print("Empate.")
        print(f"Tu capital actual es: ${capital}")
    return capital

def pedir_carta_jugador(jugador, dealer, apuesta_base, capital):
    print("Has decidido pedir una carta.")
    pidio_mano = True
    while pidio_mano and calcular_mano(jugador)[0] <= 21:
        jugador = dar_carta_jugador(jugador)
        if calcular_mano(jugador)[0] > 21:
            capital -= apuesta_base
            print(f'Cartas jugador: {jugador} \n ¡Has perdido! Tu capital actual es: ${capital}')
            break
        elif calcular_mano(jugador)[0] == 21:
            print(f'Cartas jugador: {jugador} \n ¡Tienes 21!')
            capital = plantarse(jugador, dealer, apuesta_base, capital)
            break
        else:
            print(f'Cartas jugador: {jugador} \n ¿Deseas pedir otra carta? (s/n): ')
            pidio_mano = input().lower() == 's'
    if not pidio_mano and calcular_mano(jugador)[0] < 21:
        capital = plantarse(jugador, dealer, apuesta_base, capital)
    return jugador, capital

def doblar_apuesta_jugador(jugador, dealer, apuesta_base, capital):
    print("Has decidido doblar tu apuesta.")
    nueva_apuesta = apuesta_base * 2
    jugador = dar_carta_jugador(jugador)
    print(f'Cartas jugador (doblado): {jugador}')
    if calcular_mano(jugador)[0] > 21:
        capital -= nueva_apuesta
        print(f'¡Has perdido! Tu capital actual es: ${capital}')
    else:
        capital = plantarse(jugador, dealer, nueva_apuesta, capital)
    return jugador, capital

def dividir_mano_jugador(jugador, dealer, apuesta_base, capital):
    print("Has decidido dividir tu mano.")
    mano1 = [jugador[0], obtener_carta()]
    mano2 = [jugador[1], obtener_carta()]
    capital -= apuesta_base
    print(f"Se ha descontado una apuesta extra de ${apuesta_base}. Capital actual: ${capital}")
    return mano1, mano2, capital

#Funciones de ayuda para seguro y rendición temprana
def ofrecer_seguro(apuesta_base, capital):
    respuesta = input("El dealer muestra un As. ¿Quieres comprar seguro (s/n)? ").lower()
    if respuesta == 's':
        seguro = apuesta_base // 2
        if seguro > capital:
            seguro = capital
        capital -= seguro
        print(f"Has comprado seguro por ${seguro}.")
        return seguro, capital
    return 0, capital

def resolver_seguro(seguro, dealer, capital):
    valor_dealer, _ = calcular_mano(dealer)
    if valor_dealer == 21:
        ganancia = seguro * 2
        capital += ganancia
        print(f"¡Seguro ganado! Recibes ${ganancia}. Tu capital es ahora ${capital}.")
    else:
        print("Seguro perdido.")
    return capital

def rendirse_early(apuesta_base, capital):
    devolucion = apuesta_base // 2
    capital += devolucion
    print(f"Has rendido. Recuperas la mitad de la apuesta: ${devolucion}. Tu capital actual es: ${capital}")
    return capital

# Función para re‑mezclar la shoe si quedan menos del 15% de cartas
def rebalancear_si_necesario():
    total_cartas = len(tipos_cartas) * 24
    if len(mazo) < 0.15 * total_cartas:
        print("Recreando la shoe (menos del 15 % de cartas restante).")
        nuevo_mazo()
    barajas_restantes = len(mazo) // 52
    print(f"Barajas restantes: {barajas_restantes}")
