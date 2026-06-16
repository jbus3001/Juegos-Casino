import time
import random

# Ruleta Europea: 0 (verde) + números 1-36
ruleta_europea = {
    0: "verde",
    1: "rojo", 3: "rojo", 5: "rojo", 7: "rojo", 9: "rojo", 12: "rojo",
    14: "rojo", 16: "rojo", 18: "rojo", 19: "rojo", 21: "rojo", 23: "rojo",
    25: "rojo", 27: "rojo", 30: "rojo", 32: "rojo", 34: "rojo", 36: "rojo",
    2: "negro", 4: "negro", 6: "negro", 8: "negro", 10: "negro", 11: "negro",
    13: "negro", 15: "negro", 17: "negro", 20: "negro", 22: "negro", 24: "negro",
    26: "negro", 28: "negro", 29: "negro", 31: "negro", 33: "negro", 35: "negro"
}

# Ruleta Americana: 0, 00 + números 1-36
ruleta_americana = {
    0: "verde",
    "00": "verde",
    1: "rojo", 3: "rojo", 5: "rojo", 7: "rojo", 9: "rojo", 12: "rojo",
    14: "rojo", 16: "rojo", 18: "rojo", 19: "rojo", 21: "rojo", 23: "rojo",
    25: "rojo", 27: "rojo", 30: "rojo", 32: "rojo", 34: "rojo", 36: "rojo",
    2: "negro", 4: "negro", 6: "negro", 8: "negro", 10: "negro", 11: "negro",
    13: "negro", 15: "negro", 17: "negro", 20: "negro", 22: "negro", 24: "negro",
    26: "negro", 28: "negro", 29: "negro", 31: "negro", 33: "negro", 35: "negro"
}

# Diccionario de apuestas para la ruleta
apuestas_ruleta = {
    "Americana": {
        "Straight Up": {"pago": 35, "tipo": "inside"},
        "Split": {"pago": 17, "tipo": "inside"},
        "Street": {"pago": 11, "tipo": "inside"},
        "Corner": {"pago": 8, "tipo": "inside"},
        "Line": {"pago": 5, "tipo": "inside"},
        "Five Number": {"pago": 6, "tipo": "inside"}, 
        "Color": {"pago": 1, "tipo": "outside"},
        "ParImpar": {"pago": 1, "tipo": "outside"},
        "AltoBajo": {"pago": 1, "tipo": "outside"},
        "Docena": {"pago": 2, "tipo": "outside"},
        "Columna": {"pago": 2, "tipo": "outside"}
    },
    "Europea": {
        "Straight Up": {"pago": 35, "tipo": "inside"},
        "Split": {"pago": 17, "tipo": "inside"},
        "Street": {"pago": 11, "tipo": "inside"},
        "Corner": {"pago": 8, "tipo": "inside"},
        "Line": {"pago": 5, "tipo": "inside"},
        "Color": {"pago": 1, "tipo": "outside"},
        "ParImpar": {"pago": 1, "tipo": "outside"},
        "AltoBajo": {"pago": 1, "tipo": "outside"},
        "Docena": {"pago": 2, "tipo": "outside"},
        "Columna": {"pago": 2, "tipo": "outside"}
    }
}

# Funciones auxiliares para determinar las propiedades de los números
def es_par(num_str):
    try:
        num = int(num_str)
        if num == 0: return False # 0 y 00 no son pares ni impares
        return num % 2 == 0
    except ValueError:
        return False

def es_impar(num_str):
    try:
        num = int(num_str)
        if num == 0: return False
        return num % 2 != 0
    except ValueError:
        return False

def es_alto(num_str):
    try:
        num = int(num_str)
        return 19 <= num <= 36
    except ValueError:
        return False

def es_bajo(num_str):
    try:
        num = int(num_str)
        return 1 <= num <= 18
    except ValueError:
        return False

def obtener_docena(num_str):
    try:
        num = int(num_str)
        if 1 <= num <= 12: return "1"
        elif 13 <= num <= 24: return "2"
        elif 25 <= num <= 36: return "3"
        return None
    except ValueError:
        return None

def obtener_columna(num_str):
    try:
        num = int(num_str)
        if num == 0: return None
        if num % 3 == 1: return "1"
        elif num % 3 == 2: return "2"
        elif num % 3 == 0: return "3"
        return None
    except ValueError:
        return None

def pedir_detalle_apuesta(tipo_apuesta):
    if tipo_apuesta == "Color":
        return input("¿A qué color apuestas? (rojo/negro): ").lower().strip()
    elif tipo_apuesta == "ParImpar":
        return input("¿A qué apuestas? (par/impar): ").lower().strip()
    elif tipo_apuesta == "AltoBajo":
        return input("¿A qué apuestas? (alto/bajo): ").lower().strip()
    elif tipo_apuesta in ["Docena", "Columna"]:
        return input(f"¿A qué {tipo_apuesta.lower()} apuestas? (1, 2 o 3): ").strip()
    elif tipo_apuesta == "Five Number":
        return ["0", "00", "1", "2", "3"]
    else:
        # Apuestas de números
        numeros = input(f"Ingresa los números para tu apuesta {tipo_apuesta} (separados por comas, ej. 1, 2): ")
        # Convertir a lista de strings, eliminando espacios
        return [num.strip() for num in numeros.split(",")]

# Calculo de las ganancias segun el resultado real
def procesar_resultado(tipo_apuesta, detalle, monto, resultado, color_resultado, ruleta="Europea"):
    if tipo_apuesta not in apuestas_ruleta[ruleta]:
        print("Tipo de apuesta no válido para esta ruleta.")
        return 0

    res_str = str(resultado)
    gano = False
    
    if tipo_apuesta == "Color":
        gano = (detalle == color_resultado)
    elif tipo_apuesta == "ParImpar":
        if detalle == "par" and es_par(res_str): gano = True
        elif detalle == "impar" and es_impar(res_str): gano = True
    elif tipo_apuesta == "AltoBajo":
        if detalle == "alto" and es_alto(res_str): gano = True
        elif detalle == "bajo" and es_bajo(res_str): gano = True
    elif tipo_apuesta == "Docena":
        gano = (detalle == obtener_docena(res_str))
    elif tipo_apuesta == "Columna":
        gano = (detalle == obtener_columna(res_str))
    else:
        # Apuestas específicas de números (Straight Up, Split, etc.)
        gano = res_str in detalle
        
    if gano:
        pago = apuestas_ruleta[ruleta][tipo_apuesta]["pago"]
        ganancia = monto * pago
        print(f"¡Felicidades! Acertaste. Ganaste ${ganancia} más tu apuesta inicial de ${monto}. Total: ${monto + ganancia}")
        return ganancia
    else:
        print(f"Lo siento, la apuesta no fue ganadora. Pierdes ${monto}.")
        return -monto
