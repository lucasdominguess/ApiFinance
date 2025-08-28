import telebot
import os
from dotenv import load_dotenv
from log_config import setup_logging

logger = setup_logging("telegrambot")

load_dotenv()

keyApi = os.getenv('API_TOKEN')
chat_id = os.getenv('CHAT_ID')

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(keyApi)

    def send_message(self,msg: str):
        try:
            e=self.bot.send_message(chat_id, msg,message_effect_id=True)
            #logger.warning(e.chat.id)
            # logger.info('Mensagem via telegram enviada com sucesso')
        except Exception as e:
            logger.error(f'Erro ao enviar mensagem via Telegram: {e}')
