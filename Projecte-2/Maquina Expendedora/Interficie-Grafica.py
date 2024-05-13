import RPi.GPIO as GPIO
import time
import threading
import board
import adafruit_dht
import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Bot import TelegramBot

# Defineix el pin GPIO al qual està connectat el pin SIGNAL del sensor de moviment
PIR_PIN = 18

# Configura els pins GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Inicialitza la variable per controlar l'estat de detecció
deteccio_activa = False
cocacoles_comprades = 10
coca_cola_count = 10
coca_cola_empty_notified = False  # Variable per controlar si ja s'ha enviat el missatge de coca-cola esgotada

# Creem una instància de la classe TelegramBot per a poder enviar missatges
mi_bot = TelegramBot()

# Funció per llegir la temperatura i humitat del sensor
def read_sensor_data():
    try:
        # Defineix el pin GPIO al qual està connectat el sensor DHT11
        pin = board.D4  # Canvia aquest valor si has connectat el sensor a un altre pin GPIO

        # Crear una instància del sensor DHT11
        dht_sensor = adafruit_dht.DHT11(pin)

        while True:
            # Llegeix la temperatura i la humitat des del sensor DHT11
            try:
                temperature = dht_sensor.temperature
                humidity = dht_sensor.humidity
                # Actualitza el text de l'etiqueta per mostrar la temperatura i la humitat
                temp_hum_label.config(text=f'Temperatura: {temperature:.1f} °C, Humitat: {humidity:.1f} %')
            except RuntimeError as e:
                # Captura errors de lectura del sensor
                temp_hum_label.config(text='Error en llegir el sensor. Torna a intentar...')
            time.sleep(2)
    except KeyboardInterrupt:
        pass

# Funció per a gestionar la detecció de moviment i la compra de Coca-Colas
def detect_motion():
    global deteccio_activa, cocacoles_comprades, coca_cola_count, coca_cola_empty_notified
    try:
        while True:
            if GPIO.input(PIR_PIN):
                if not deteccio_activa and coca_cola_count > 0:
                    print("S'ha detectat moviment! S'ha comprat una Coca-Cola.")
                    coca_cola_count -= 1
                    deteccio_activa = True

                    # Actualitza la visualització del nombre de Coca-Colas restants
                    coca_cola_label.config(text=f'Coca-Colas restants: {coca_cola_count}')

                    # Comprova si cal enviar un missatge al bot de Telegram
                    if coca_cola_count == 4:  # Comprova si ara hi ha 4 Coca-Colas
                        mi_bot.enviar_mensaje("Només queden 4 Coca-Colas. Caldrà reposar la màquina.")
                    elif coca_cola_count == 0:
                        mi_bot.enviar_mensaje("No queden Coca-Colas! Cal urgir el reompliment de la màquina.")

                elif coca_cola_count == 0 and not coca_cola_empty_notified:
                    print("No queden Coca-Colas disponibles. No es poden comprar més.")
                    coca_cola_empty_notified = True
            else:
                deteccio_activa = False
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# Funció per a reposar Coca-Colas
def refill_coca_colas():
    global coca_cola_count, coca_cola_empty_notified
    try:
        refill_value = int(refill_entry.get())
        previous_count = coca_cola_count
        coca_cola_count += refill_value
        refill_entry.delete(0, 'end')  # Esborra el contingut del camp d'entrada
        coca_cola_label.config(text=f'Coca-Colas restants: {coca_cola_count}')

        # Notifiquem al bot de Telegram la reposició de Coca-Colas
        mi_bot.enviar_mensaje(f"S'han reposat {refill_value} Coca-Colas.")

        # Comprova si la màquina estava buida i ara hi ha Coca-Colas
        if previous_count == 0 and coca_cola_count > 0:
            mi_bot.enviar_mensaje("La màquina s'ha reposat amb Coca-Colas. Ara hi ha disponibles.")
            coca_cola_empty_notified = False  # Reinicialitza el flag de notificació
    except ValueError:
        pass

# Inicialitza una finestra de GUI
root = tk.Tk()
root.title("Venda de Coca-Colas")

# Creem etiquetes per mostrar la temperatura i la humitat
temp_hum_label = tk.Label(root, text="")
temp_hum_label.pack()

# Creem una etiqueta per mostrar el nombre de Coca-Colas restants
coca_cola_label = tk.Label(root, text=f'Coca-Colas restants: {coca_cola_count}')
coca_cola_label.pack()

# Creem un camp d'entrada per a la reposició de Coca-Colas
refill_frame = tk.Frame(root)
refill_frame.pack()
refill_label = tk.Label(refill_frame, text="Reposar Coca-Colas:")
refill_label.pack(side="left")
refill_entry = tk.Entry(refill_frame)
refill_entry.pack(side="left")
refill_button = tk.Button(refill_frame, text="Reposar", command=refill_coca_colas)
refill_button.pack(side="left")

# Inicia un fil per llegir la temperatura i humitat
sensor_thread = threading.Thread(target=read_sensor_data)
sensor_thread.daemon = True
sensor_thread.start()

# Inicia un fil per detectar el moviment i gestionar la compra de Coca-Colas
motion_thread = threading.Thread(target=detect_motion)
motion_thread.daemon = True
motion_thread.start()

# Inicia el bucle principal de l'aplicació GUI
root.mainloop()
