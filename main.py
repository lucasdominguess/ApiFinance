import yfinance as yf
import os
from telegrambot import TelegramBot
import dotenv
from log_config import setup_logging

logger = setup_logging("telegrambot")
dotenv.load_dotenv()
keyApi = os.getenv('API_TOKEN')

try:
    tickets = [ 
        "PETR4.SA",
        "SNLG11.SA"
        "KEPL3.SA",
        "SEQL3.SA",
        "CASH3.SA",
        "DASA3.SA",
        "RNEW4.SA",
        "CAML3.SA",
        "HAPV3.SA",
        "JSLG3.SA",
        "MTRE3.SA",
        "BPAN4.SA"
    ]
    for ticket in tickets:
        ticket = yf.Ticker(ticket)
        info = ticket.info

        # info_data = [
        #     f"Nome da Ação: {info.get('shortName')}",
        #     f"Simbolo: {info.get('symbol')}",
        #     f"Preço atual (R$): {info.get('regularMarketPrice')}",
        #     f"Variação no dia (%): {info.get('regularMarketChangePercent')}",
        # ]

        message = f"Simbolo: {info.get('symbol')} -Preço atual (R$): {info.get('regularMarketPrice')}",
        
        bot = TelegramBot()
        bot.send_message(message)
        print(message)
        logger.info(f"Informações da ação {info.get('symbol')}: {message}")
except Exception as e:
    logger.error(f"\nDetalhes do erro: {e}")
    print(f"Erro ao obter informações da ação: {ticket}\nDetalhes do erro: {e}")
