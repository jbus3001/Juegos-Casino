import Funciones_Casino as fb

capital= 1000
respuesta_jugador=True
pidio_mano = True
#Preparamos la mesa y el mazo
fb.nuevo_mazo()
fb.preparar_mesa()
print("¡A perder dinero con el BlackJack!\n Cuentas con un capital base de  $1000, el pago por BlackJack es de 3:2.\n")

#El juego se repetirá hasta que el jugador decida salir o se quede sin capital.
while respuesta_jugador and capital >=0:
    pidio_mano = True

    #Eleginos la apuesta del jugador con un minimo de $10 y un máximo de $500 por mano.
    apuesta_base = int(input("¿Cuánto deseas apostar por mano? (mínimo $10, máximo $500): "))
    while apuesta_base < 10 or apuesta_base > 500:
        print("Apuesta inválida. Por favor, ingresa un monto entre $10 y $500.")
        apuesta_base = int(input("¿Cuánto deseas apostar por mano? (mínimo $10, máximo $500): "))

    #Repartimos manos
    jugador, dealer = fb.repartir_manos_inicio()

    # Calculamos el valor de las manos iniciales verificando Blackjack
    jugador_bj = fb.calcular_mano(jugador)[0] == 21
    dealer_bj = fb.calcular_mano(dealer)[0] == 21

    if jugador_bj and dealer_bj:
        print(f'Cartas dealer: {dealer}')
        print(f'Cartas jugador: {jugador}')
        print("¡Empate! Ambos tienen BlackJack.")
    elif jugador_bj:
        print(f'Cartas jugador: {jugador} \n')
        print("¡BlackJack! Has ganado 1.5 veces tu apuesta.")
        capital += int(apuesta_base * 1.5)  
    elif dealer_bj:
        print(f'Cartas dealer: {dealer}')
        print(f'Cartas jugador: {jugador}')
        print("¡El dealer tiene BlackJack! Has perdido.")
        capital -= apuesta_base
    else:
        # Ninguno tiene Blackjack, el juego continúa
        #Mostramos las cartas del dealer y del jugador, ocultando la segunda carta del dealer.
        print(f'Cartas dealer: {dealer[0]} y ⍍ \n ')
        print(f'Cartas jugador: {jugador[0]} y {jugador[1]} \n ¿Qué deseas hacer? ')
        print("1. Plantarse")
        print("2. Pedir carta")
        
        opciones_validas = [1, 2]
        if apuesta_base * 2 <= capital:
            print("3. Doblar")
            opciones_validas.append(3)
        if jugador[0] == jugador[1] and apuesta_base * 2 <= capital:
            print("4. Dividir")
            opciones_validas.append(4)

        #Pedimos la acción del jugador.
        respuesta = int(input())
        while respuesta not in opciones_validas:
            print("Opción inválida. Por favor, elige una opción válida.")
            respuesta = int(input())

        #Procesamos la acción del jugador.
        if respuesta == 1:
            capital=fb.plantarse(jugador,dealer,apuesta_base,capital)
        elif respuesta == 2:
            print("Has decidido pedir una carta.")
            while pidio_mano and fb.calcular_mano(jugador)[0] <= 21:
                jugador = fb.dar_carta_jugador(jugador)
                if fb.calcular_mano(jugador)[0] > 21:
                    capital -= apuesta_base
                    print(f'Cartas jugador: {jugador} \n ¡Has perdido! Tu capital actual es: ${capital}')
                    break
                else:
                    print(f'Cartas jugador: {jugador} \n ¿Deseas pedir otra carta? (s/n): ')
                    pidio_mano = input().lower() == 's'
            if not pidio_mano:
                capital =fb.plantarse(jugador,dealer,apuesta_base,capital)
        elif respuesta == 3: 
            print("Has decidido doblar tu apuesta.")
            nueva_apuesta = apuesta_base * 2
            jugador = fb.dar_carta_jugador(jugador)
            print(f'Cartas jugador (doblado): {jugador}')
            if fb.calcular_mano(jugador)[0] > 21:
                capital -= nueva_apuesta
                print(f'¡Has perdido! Tu capital actual es: ${capital}')
            else:
                capital = fb.plantarse(jugador, dealer, nueva_apuesta, capital)
        elif respuesta == 4:
            print("Has decidido dividir tu mano.")
            mano1 = [jugador[0], fb.obtener_carta()]
            mano2 = [jugador[1], fb.obtener_carta()]
            
            for i, mano_actual in enumerate([mano1, mano2], start=1):
                print(f'\n--- Jugando Mano {i} ---')
                print(f'Cartas Mano {i}: {mano_actual}')
                pidio_mano = input(f"¿Deseas pedir carta para la Mano {i}? (s/n): ").lower() == 's'
                
                while pidio_mano and fb.calcular_mano(mano_actual)[0] <= 21:
                    mano_actual = fb.dar_carta_jugador(mano_actual)
                    if fb.calcular_mano(mano_actual)[0] > 21:
                        capital -= apuesta_base
                        print(f'Cartas Mano {i}: {mano_actual} \n ¡Has perdido la Mano {i}! Tu capital actual es: ${capital}')
                        break
                    else:
                        print(f'Cartas Mano {i}: {mano_actual}')
                        pidio_mano = input("¿Deseas pedir otra carta? (s/n): ").lower() == 's'
                
                if fb.calcular_mano(mano_actual)[0] <= 21:
                    capital = fb.plantarse(mano_actual, dealer, apuesta_base, capital)

    if capital > 0:
        respuesta_jugador = input("¿Deseas jugar otra mano? (s/n): ").lower() == 's'
    else:
        print("Te has quedado sin capital. ¡Fin del juego!")
        break


            