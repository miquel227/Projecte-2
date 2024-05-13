import time
import board
import adafruit_dht

# Definir el pin GPIO al qual està connectat el sensor DHT11
pin = board.D4  # Canvia aquest valor si has connectat el sensor a un altre pin GPIO

# Crear una instància del sensor DHT11
dht_sensor = adafruit_dht.DHT11(pin)

try:
    while True:
        # Llegeix la temperatura i la humitat des del sensor DHT11
        try:
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity
            print('Temperatura: {0:0.1f} °C - Humitat: {1:0.1f} %'.format(temperature, humidity), end='\r')
        except RuntimeError as e:
            # Captura errors de lectura del sensor
            print('Error en llegir el sensor. Torna a intentar...', end='\r')
            continue
        
        # Espera 2 segons abans de fer la següent lectura
        time.sleep(2)
except KeyboardInterrupt:
    # Atura el programa si es prem Control + C
    print("\nPrograma aturat.")
