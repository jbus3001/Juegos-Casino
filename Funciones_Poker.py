import random
import time

#Creamos la baraja de cartas, asi como su asignacion de valores para el juego
baraja = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
palos = ['♡', '♢', '♣', '♠']
valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

#Creamos la baraja completa y la mezclamos
def crear_baraja():
    baraja_completa = [(valor, palo) for valor in baraja for palo in palos]
    random.shuffle(baraja_completa)
    return baraja_completa

#Repartimos las cartas iniciales al jugador i
def pre_flop(baraja, i):
    mano_jugador = [baraja.pop(), baraja.pop()]
    return mano_jugador

#realizamos el flop, turn y river
def repartir_flop_turn_river(baraja):
    flop = [baraja.pop(), baraja.pop(), baraja.pop()]
    turn = baraja.pop()
    river = baraja.pop()
    return flop, turn, river

