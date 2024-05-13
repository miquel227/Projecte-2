import RPi.GPIO as GPIO
import time

# Defineix el pin GPIO al qual està connectat el pin SIGNAL del sensor
PIR_PIN = 18

# Configura els pins GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Inicialitza la variable per controlar l'estat de detecció
deteccio_activa = False

try:
    print("Esperant moviment...")
    while True:
        if GPIO.input(PIR_PIN):
            if not deteccio_activa:
                print("S'ha detectat moviment! S'ha comprat una Coca-Cola.")
                deteccio_activa = True
            # Aquí pots afegir la lògica per restar un número o fer qualsevol altra acció
        else:
            deteccio_activa = False  # Restableix l'estat de detecció
        time.sleep(0.1)  # Espera 0.1 segons abans de tornar a comprovar
except KeyboardInterrupt:
    print("\nS'ha interromput l'execució del programa.")
finally:
    GPIO.cleanup()  # Restaura la configuració dels pins GPIO
