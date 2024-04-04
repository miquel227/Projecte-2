##Coca-cola
import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
from Bot import TelegramBot

class MaquinaExpendora:
    def __init__(self):
        self.cantidad_cocacolas = 10
        self.bot = TelegramBot()  # Creem una instància del teu bot de Telegram
        self.intents_de_compra = 0
        self.avisa_esgotament = False

    def comprar_cocacola(self):
        if self.cantidad_cocacolas > 0:
            self.cantidad_cocacolas -= 1
            mensaje = "Has comprat una Coca-Cola. Gaudeix-la!"
            print(mensaje)  # Mostrem el missatge a la pantalla de la màquina
            if self.cantidad_cocacolas == 4:
                mensaje_telegram = "Només queden 4 Coca-Colas a la màquina expendedora 1 de Tortosa. Avis per repostar."
                self.bot.enviar_mensaje(mensaje_telegram)  # Enviem la notificació al bot de Telegram
        elif self.avisa_esgotament:
            self.intents_de_compra += 1
            mensaje_terminal = "Ho sentim, ja no queden Coca-Colas disponibles."
            print(mensaje_terminal)  # Mostrem el missatge a la pantalla de la màquina
            mensaje_telegram = f"Intent número {self.intents_de_compra} de compra de Coca-Cola."
            self.bot.enviar_mensaje(mensaje_telegram)  # Enviem la notificació al bot de Telegram
        else:
            self.avisa_esgotament = True
            mensaje_terminal = "Ho sentim, ja no queden Coca-Colas disponibles."
            print(mensaje_terminal)  # Mostrem el missatge a la pantalla de la màquina
            mensaje_telegram = f"S'han esgotat les Coca-Colas a la Màquina-Expendedora-1 de Tortosa. S'han de reposar immediatament!!!!!"
            self.bot.enviar_mensaje(mensaje_telegram)  # Enviem la notificació al bot de Telegram

if __name__ == "__main__":
    maquina = MaquinaExpendora()
    while True:
        opcion = input("Prem 1 per comprar una Coca-Cola o 0 per sortir: ")
        if opcion == "1":
            maquina.comprar_cocacola()
        elif opcion == "0":
            print("Gràcies per usar la nostra màquina expendedora. ¡Adéu!")
            break
        else:
            print("Opció invàlida. Si us plau, prem 1 per comprar o 0 per sortir.")


