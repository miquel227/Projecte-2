import RPi.GPIO as GPIO
import time

class MaquinaExpendora:
    def __init__(self):
        self.cantidad_cocacolas = 10
        self.intents_de_compra = 0
        self.avisa_esgotament = False

        # Configurar el pin del sensor de moviment
        self.sensor_pin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    def comprar_cocacola(self):
        if self.cantidad_cocacolas > 0:
            self.cantidad_cocacolas -= 1
            mensaje = "Has comprat una Coca-Cola. Gaudeix-la!"
            print(mensaje)  # Mostrem el missatge a la pantalla de la màquina
            if self.cantidad_cocacolas == 4:
                mensaje_telegram = "Només queden 4 Coca-Colas a la màquina expendedora 1 de Tortosa. Avis per repostar."
                # self.bot.enviar_mensaje(mensaje_telegram)  # Enviem la notificació al bot de Telegram
        elif self.avisa_esgotament:
            self.intents_de_compra += 1
            mensaje_terminal = "Ho sentim, ja no queden Coca-Colas disponibles."
            print(mensaje_terminal)  # Mostrem el missatge a la pantalla de la màquina
            mensaje_telegram = f"Intent número {self.intents_de_compra} de compra de Coca-Cola."
            # self.bot.enviar_mensaje(mensaje_telegram)  # Enviem la notificació al bot de Telegram
        else:
            self.avisa_esgotament = True
            mensaje_terminal = "Ho sentim, ja no queden Coca-Colas disponibles."
            print(mensaje_terminal)  # Mostrem el missatge a la pantalla de la màquina
            mensaje_telegram = f"S'han esgotat les Coca-Colas a la Màquina-Expendedora-1 de Tortosa. S'han de reposar immediatament!!!!!"
            # self.bot.enviar_mensaje(mensaje_telegram)  # Enviem la notificació al bot de Telegram

if __name__ == "__main__":
    maquina = MaquinaExpendora()
    try:
        while True:
            # Esperar que es detecti un moviment
            if GPIO.input(maquina.sensor_pin):
                maquina.comprar_cocacola()
                time.sleep(2)  # Esperar 2 segons per evitar deteccions múltiples
    finally:
        GPIO.cleanup()
