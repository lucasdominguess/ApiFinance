import yfinance as yf
import os
from telegrambot import TelegramBot
import dotenv
from log_config import setup_logging

logger = setup_logging("telegrambot")
dotenv.load_dotenv()
keyApi = os.getenv('API_TOKEN')

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

tickers2 = [
     "ITUB3.SA",
    "ITUB4.SA",
    "CXSE3.SA",
    "VULC3.SA",
    "MTRE3.SA",
    "JHSF3.SA",
    "MDIA3.SA",
    "BEES3.SA",
    "BEES4.SA",
    "ITSA3.SA",
    "ITSA4.SA",
    "BBDC4.SA",
    "ITUB4.SA",
    "BBDC3.SA",
    "QUAL3.SA",
    "CRFB3.SA",
    "MTRE3.SA",
    "VULC3.SA",
    "MDNE3.SA",
    "ALOS3.SA",
    "MDIA3.SA",
    "VIVT3.SA",
    "JHSF3.SA",
    "ITSA4.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "PETR4.SA",
    "BBAS3.SA",    
    "KEPL3.SA",
    "SEQL3.SA",
    "CASH3.SA",
    "DASA3.SA",
    "RNEW4.SA",
    "CAML3.SA",
    "HAPV3.SA",
    "JSLG3.SA",
    "BPAN4.SA",
    ]   
try:
 
    bot = TelegramBot()
    print("Iniciando busca das ações")
    logger.info("Iniciando busca das ações")
    for tick in tickers2:
        Ticker = yf.Ticker(tick)
        hist = Ticker.history(period="1mo", interval="1d")
        info = Ticker.info
        Price = info.get("regularMarketPrice")
        
        print(f' Ticker: {tick}  Preço atual R$: {Price} \n')

        if Price <= 10 or tick == "PETR4.SA":
            bot.send_message(f'Ticker: {tick} Preço atual R$:{Price} \n')
            print(f' Ticker: {tick}  Preço atual R$: {Price} \n')
        else:
            print(f' Ticker: {tick}  Preço atual R$: {Price} \n')
        
        # bot.send_message(f' Ticker: {tick} Preço atual R$:{Price} \n')
    logger.info("Busca das ações concluida")
    print("Busca das ações concluida")
except Exception as e:
             print(f"Erro ao obter informações da ação: {Ticker}\n Detalhes do erro: {e}")
             logger.error(f"Erro ao obter informações da ação: {Ticker} \n Detalhes do erro: {e}")
             bot.send_message(f"Erro ao obter informações da ação: {Ticker}\nDetalhes do erro: {e}")
