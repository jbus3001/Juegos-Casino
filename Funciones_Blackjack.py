import random
import time

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
def plantarse(jugador,dealer,apuesta_base,capital):
    print("Has decidido plantarte.")
    print('La mano del dealer es: ')
    dealer_final = evaluacion_mano_dealer(dealer)
    print(dealer_final)
    
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
