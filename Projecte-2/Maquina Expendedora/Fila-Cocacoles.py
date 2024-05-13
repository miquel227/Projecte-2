import RPi.GPIO as GPIO
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Bot import TelegramBot  # Importa la classe del teu bot de Telegram

# Defineix el pin GPIO al qual està connectat el pin SIGNAL del sensor
PIR_PIN = 18

# Configura els pins GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Inicialitza la variable per controlar l'estat de detecció
deteccio_activa = False
cocacoles_comprades = 0
coca_cola_count = 10
coca_cola_empty_notified = False  # Variable per controlar si ja s'ha enviat el missatge de coca-cola esgotada

# Creem una instància de la classe TelegramBot per a poder enviar missatges
mi_bot = TelegramBot()

try:
    print("Esperant moviment...")
    while True:
        if coca_cola_count > 0:  # Comprova si hi ha Coca-Colas disponibles
            if GPIO.input(PIR_PIN):
                if not deteccio_activa:
                    print("S'ha detectat moviment! S'ha comprat una Coca-Cola." )
                    print(f"Nombre de Coca-Colas restants: {coca_cola_count}")
                    coca_cola_count -= 1
                    cocacoles_comprades += 1
                    deteccio_activa = True

                    # Comprovem si cal enviar un missatge al bot de Telegram
                    if cocacoles_comprades == 6:
                        mi_bot.enviar_mensaje("Només queden 4 Coca-Colas. Caldrà repostar la màquina.")
                    elif cocacoles_comprades == 10:
                        mi_bot.enviar_mensaje("No queden Coca-Colas! Cal urgir el reompliment de la màquina.")
                # Aquí pots afegir la lògica per restar un número o fer qualsevol altra altra acció
            else:
                deteccio_activa = False  # Restableix l'estat de detecció
            time.sleep(0.1)  # Espera 0.1 segons abans de tornar a comprovar
        else:
            if not coca_cola_empty_notified:
                print("No queden Coca-Colas disponibles. No es poden comprar més.")
                coca_cola_empty_notified = True  # Marca que ja s'ha enviat el missatge
            time.sleep(1)  # Espera 1 segon abans de tornar a comprovar
except KeyboardInterrupt:
    print("\nS'ha interromput l'execució del programa.")
finally:
    GPIO.cleanup()  # Restaura la configuració dels pins GPIO
