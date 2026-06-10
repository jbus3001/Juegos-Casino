import Funciones_Casino as fb

capital= 1000
respuesta_jugador=True
pidio_mano = True
#Preparamos la mesa y el mazo
fb.nuevo_mazo()
fb.preparar_mesa()
print("¡A perder dinero con el BlackJack!\n Cuentas con un capital base de  $1000, el pago por BlackJack es de 3:2.\n")

#El juego se repetirá hasta que el jugador decida salir o se quede sin capital.
while respuesta_jugador and capital >0:
    pidio_mano = True

    #Eleginos la apuesta del jugador con un minimo de $10 y un máximo de $500 por mano.
    apuesta_base = int(input("¿Cuánto deseas apostar por mano? (mínimo $10, máximo $500): "))
    while apuesta_base < 10 or apuesta_base > 500:
        print("Apuesta inválida. Por favor, ingresa un monto entre $10 y $500.")
        apuesta_base = int(input("¿Cuánto deseas apostar por mano? (mínimo $10, máximo $500): "))

    #Repartimos manos
    jugador, dealer = fb.repartir_manos_inicio()

    #Calculamos el valor de las manos iniciales
    # Si el jugador tiene BlackJack, gana automáticamente.
    if fb.calcular_mano(jugador)[0] == 21:
        print(f'cartas jugador: {jugador} \n')
        print("¡BlackJack! Has ganado 1.5 veces tu apuesta.")
        capital += int(apuesta_base * 1.5)  
    else:
        #Mostramos las cartas del dealer y del jugador, ocultando la segunda carta del dealer.
        print(f'Cartas dealer: {dealer[0]} y ⍍ \n ')
        print(f'Cartas jugador: {jugador[0]} y {jugador[1]} \n ¿Qué deseas hacer? ')
        print("1. Plantarse")
        print("2. Pedir carta")
        print("3. Doblar")
        if jugador[0] == jugador[1]:
            print("4. Dividir")

        #Pedimos la acción del jugador.
        respuesta= int(input())
        while respuesta not in [1, 2, 3, 4] or (respuesta == 4 and jugador[0] != jugador[1]):
            print("Opción inválida. Por favor, elige una opción válida.")
            respuesta= int(input())

        #Procesamos la acción del jugador.
        if respuesta == 1:
            fb.plantarse(jugador,dealer,apuesta_base,capital)
            respuesta_jugador = input("¿Deseas jugar otra mano? (s/n): ").lower() == 's'
        elif respuesta == 2:
            print("Has decidido pedir una carta.")
            while pidio_mano and fb.calcular_mano(jugador)[0] <= 21:
                jugador = fb.dar_carta_jugador(jugador)
                if fb.calcular_mano(jugador)[0] > 21:
                    capital -= apuesta_base
                    print(f'Cartas jugador: {jugador} \n ¡Has perdido! Tu capital actual es: ${capital}')
                    respuesta_jugador = input("¿Deseas jugar otra mano? (s/n): ").lower() == 's'
                    break
                else:
                    print(f'Cartas jugador: {jugador} \n ¿Deseas pedir otra carta? (s/n): ')
                    pidio_mano = input().lower() == 's'
            if not pidio_mano:
                capital = fb.plantarse(jugador,dealer,apuesta_base,capital)
                respuesta_jugador = input("¿Deseas jugar otra mano? (s/n): ").lower() == 's'
        

            