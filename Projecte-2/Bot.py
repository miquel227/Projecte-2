import requests

# Creem la classe TelegramBot per a poder enviar missatges i documents al bot de Telegram
class TelegramBot:
    def __init__(self):
        # Definim el token i el chat_id del nostre bot de Telegram
        self.token = '6889677932:AAHlD9wD_ErIn7rD8nvlHGC7-7eKY8NzHEE'
        self.chat_id = '-1002143597676'
    # Definim els mètodes per a enviar missatges
    def enviar_mensaje(self, mensaje):
        response = requests.post(
            'https://api.telegram.org/bot' + self.token + '/sendMessage',
            data={'chat_id': self.chat_id, 'text': mensaje, 'parse_mode': 'HTML'}
        )
        # if response.status_code == 200:
        #     print('El missatge s\'ha enviat correctament.')
        # else:
        #     print('El missatge no s\'ha pogut enviar.')
    # Definim el mètode per a enviar documents
    def enviar_document(self, document_path):
        with open(document_path, 'rb') as doc_file:
            response = requests.post(
                'https://api.telegram.org/bot' + self.token + '/sendDocument',
                data={'chat_id': self.chat_id},
                files={'document': doc_file}
            )
            if response.status_code == 200:
                print('El document amb els resultats s\'ha enviat correctament.')
            else:
                print('El document amb els resultats no s\'ha pogut enviar.')
    # Definim el mètode per a enviar missatges
    def mensaje(self, text):
        self.enviar_mensaje(text)
# Creem una instància de la classe TelegramBot per a poder enviar missatges i documents al bot de Telegram
mi_bot = TelegramBot()