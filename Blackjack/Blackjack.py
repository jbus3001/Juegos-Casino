import Funciones_Blackjack as fb

capital= 1000
respuesta_jugador=True
pidio_mano = True
#Preparamos la mesa y el mazo
fb.nuevo_mazo()
fb.rebalancear_si_necesario()
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
    # --- Seguro (insurance) ---
    seguro = 0
    if dealer[0] == 'A':
        seguro, capital = fb.ofrecer_seguro(apuesta_base, capital)

    jugador_bj = fb.calcular_mano(jugador)[0] == 21
    dealer_bj = fb.calcular_mano(dealer)[0] == 21

    if jugador_bj and dealer_bj:
        print(f'Cartas dealer: {dealer}')
        print(f'Cartas jugador: {jugador}')
        print("¡Empate! Ambos tienen BlackJack.")
        # En caso de empate, el seguro se pierde porque el dealer tiene Blackjack.
        if seguro > 0:
            capital = fb.resolver_seguro(seguro, dealer, capital)
    elif jugador_bj:
        print(f'Cartas jugador: {jugador} \n')
        print("¡BlackJack! Has ganado 1.5 veces tu apuesta.")
        capital += int(apuesta_base * 1.5)
    elif dealer_bj:
        print(f'Cartas dealer: {dealer}')
        print(f'Cartas jugador: {jugador}')
        print("¡El dealer tiene BlackJack! Has perdido.")
        capital -= apuesta_base
        if seguro > 0:
            capital = fb.resolver_seguro(seguro, dealer, capital)
    else:
        # Ninguno tiene Blackjack, el juego continúa
        #Mostramos las cartas del dealer y del jugador, ocultando la segunda carta del dealer.
        print(f'Cartas dealer: {dealer[0]} y ⍍ \n ')
        print(f'Cartas jugador: {jugador[0]} y {jugador[1]} \n ¿Qué deseas hacer? ')
        print("0. Rendirse (entrega mitad de la apuesta)")
        print("1. Plantarse")
        print("2. Pedir carta")
        
        opciones_validas = [0, 1, 2]
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
        if respuesta == 0:
            capital = fb.rendirse_early(apuesta_base, capital)
        elif respuesta == 1:
            capital = fb.plantarse(jugador, dealer, apuesta_base, capital)
        elif respuesta == 2:
            jugador, capital = fb.pedir_carta_jugador(jugador, dealer, apuesta_base, capital)
        elif respuesta == 3:
            jugador, capital = fb.doblar_apuesta_jugador(jugador, dealer, apuesta_base, capital)
        elif respuesta == 4:
            mano1, mano2, capital = fb.dividir_mano_jugador(jugador, dealer, apuesta_base, capital)
            capital = fb.plantarse(mano1, dealer, apuesta_base, capital, skip_dealer=True)
            capital = fb.plantarse(mano2, dealer, apuesta_base, capital, skip_dealer=False)

    if capital > 0:
        respuesta_jugador = input("¿Deseas jugar otra mano? (s/n): ").lower() == 's'
    else:
        print("Te has quedado sin capital. ¡Fin del juego!")
        break