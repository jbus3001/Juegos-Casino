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

#Calculo de las ganancias segun el tipo de apuesta
def calcular_ganancia(apuesta, monto, ruleta="Europea"):
    if apuesta in apuestas_ruleta[ruleta]:
        pago = apuestas_ruleta[ruleta][apuesta]["pago"]
        ganancia = monto * pago
        print(f"Ganaste {ganancia}€ más tu apuesta inicial de {monto}€. Total: {monto + ganancia}€")
        return ganancia
    else:
        print("Tipo de apuesta no válido para esta ruleta.")
        return 0