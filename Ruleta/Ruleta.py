import Funciones_Ruleta as fr
import time
import random   

print("Bienvenido al juego de la Ruleta")
# Seleccionamos el tipo de ruleta
tipo_ruleta = input("Selecciona el tipo de ruleta (Americana/Europea): ").strip().capitalize()
while tipo_ruleta not in ["Americana", "Europea"]:
    print("Tipo de ruleta no válido. Por favor, selecciona Americana o Europea.")
    tipo_ruleta = input("Selecciona el tipo de ruleta (Americana/Europea): ").strip().capitalize()

# Iniciamos el juego
capital = 1000
print(f"\n¡A perder dinero en la Ruleta! Empiezas con un capital de ${capital}.\n")

while True:
    # Solicitamos al jugador que realice su apuesta
    apuesta = input("Realiza tu apuesta (Straight Up, Split, Street, Corner, Line, Five Number, Color, ParImpar, AltoBajo, Docena, Columna): ")
    while apuesta not in fr.apuestas_ruleta[tipo_ruleta]:
        print("Tipo de apuesta no válido. Por favor, selecciona una apuesta válida.")
        apuesta = input("Realiza tu apuesta (Straight Up, Split, Street, Corner, Line, Five Number, Color, ParImpar, AltoBajo, Docena, Columna): ")
    
    detalle_apuesta = fr.pedir_detalle_apuesta(apuesta)
    
    monto = float(input(f"Tienes ${capital}. Ingresa el monto de tu apuesta: "))
    while monto > capital or monto <= 0:
        print("Monto inválido. No puedes apostar más de tu capital ni una cantidad nula o negativa.")
        monto = float(input(f"Tienes ${capital}. Ingresa el monto de tu apuesta: "))
    
    # Simulamos la ruleta
    print("\nGirando la ruleta...")
    time.sleep(1)
    
    resultado = random.choice(list(fr.ruleta_americana.keys()) if tipo_ruleta == "Americana" else list(fr.ruleta_europea.keys()))
    color_resultado = fr.ruleta_americana[resultado] if tipo_ruleta == "Americana" else fr.ruleta_europea[resultado]
    
    print(f"La ruleta ha caído en: {resultado} ({color_resultado})\n")
    
    # Calculamos las ganancias o perdidas
    cambio = fr.procesar_resultado(apuesta, detalle_apuesta, monto, resultado, color_resultado, tipo_ruleta)
    capital += cambio
    print(f"Tu capital actual es: ${capital}\n")
    
    if capital <= 0:
        print("Te has quedado sin capital. ¡Fin del juego!")
        break
    
    # Preguntamos si el jugador quiere seguir jugando
    seguir_jugando = input("¿Quieres seguir jugando? (s/n): ")
    if seguir_jugando.lower() != 's':
        print(f"Gracias por jugar a la Ruleta. Te retiras con ${capital}. ¡Hasta la próxima!")
        break