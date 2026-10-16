import telebot
import os
from dotenv import load_dotenv
from log_config import setup_logging

logger = setup_logging("telegrambot")

load_dotenv()


class TelegramBot:
    """
    Bot do Telegram configurável por script.

    Cada script informa os nomes das variáveis de ambiente (.env) que contêm
    o token do bot e o id do grupo/chat. Sem parâmetros, usa a configuração
    padrão (API_TOKEN / CHAT_ID).

    Exemplo:
        TelegramBot()  # bot e grupo padrão
        TelegramBot(token_env="BOT_TOKEN_PYTHON_SEARCH", chat_id_env="CHAT_ID_SMALLCAP")
    """

    def __init__(self, token_env: str = "API_TOKEN", chat_id_env: str = "CHAT_ID"):
        token = os.getenv(token_env)
        self.chat_id = os.getenv(chat_id_env)

        if not token:
            raise ValueError(f"Variável de ambiente '{token_env}' (token do bot) não definida no .env")
        if not self.chat_id:
            raise ValueError(f"Variável de ambiente '{chat_id_env}' (id do chat) não definida no .env")

        self.bot = telebot.TeleBot(token)

    def send_message(self, msg: str):
        try:
            self.bot.send_message(self.chat_id, msg)
            # logger.info('Mensagem via telegram enviada com sucesso')
        except Exception as e:
            logger.error(f'Erro ao enviar mensagem via Telegram (chat {self.chat_id}): {e}')
