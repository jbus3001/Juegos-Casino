import Funciones_Ruleta as fr
import time
import random   

print("Bienvenido al juego de la Ruleta")
# Seleccionamos el tipo de ruleta
tipo_ruleta = input("Selecciona el tipo de ruleta (Americana/Europea): ")
while tipo_ruleta not in ["Americana", "Europea"]:
    print("Tipo de ruleta no válido. Por favor, selecciona Americana o Europea.")
    tipo_ruleta = input("Selecciona el tipo de ruleta (Americana/Europea): ")

# Iniciamos el juego
while True:
    # Solicitamos al jugador que realice su apuesta
    apuesta = input("Realiza tu apuesta (Straight Up, Split, Street, Corner, Line, Five Number, Color, ParImpar, AltoBajo, Docena, Columna): ")
    while apuesta not in fr.apuestas_ruleta[tipo_ruleta]:
        print("Tipo de apuesta no válido. Por favor, selecciona una apuesta válida.")
        apuesta = input("Realiza tu apuesta (Straight Up, Split, Street, Corner, Line, Five Number, Color, ParImpar, AltoBajo, Docena, Columna): ")
    
    monto = float(input("Ingresa el monto de tu apuesta: "))
    
    # Simulamos la ruleta
    resultado = random.choice(list(fr.ruleta_americana.keys()) if tipo_ruleta == "Americana" else list(fr.ruleta_europea.keys()))
    color_resultado = fr.ruleta_americana[resultado] if tipo_ruleta == "Americana" else fr.ruleta_europea[resultado]
    
    print(f"La ruleta ha caído en: {resultado} ({color_resultado})")
    
    # Calculamos las ganancias
    fr.calcular_ganancia(apuesta, monto, tipo_ruleta)
    
    # Preguntamos si el jugador quiere seguir jugando
    seguir_jugando = input("¿Quieres seguir jugando? (s/n): ")
    if seguir_jugando.lower() != 's':
        print("Gracias por jugar a la Ruleta. ¡Hasta la próxima!")
        break