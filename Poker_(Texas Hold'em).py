import Funciones_Poker as fp

print("Bienvenido al juego de Poker (Texas Hold'em)")
# Creamos la baraja y la mezclamos
baraja = fp.crear_baraja()
# Repartimos las cartas a los jugadores
for i in range(5):
    mano_jugador = [baraja.pop(), baraja.pop()]
  #  print(f"Jugador {i+1} tiene: {mano_jugador[0][0]}{mano_jugador[0][1]} y {mano_jugador[1][0]}{mano_jugador[1][1]}")
print(mano_jugador)