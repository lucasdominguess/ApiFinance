import yfinance as yf
import csv
import os
from telegrambot import TelegramBot
import dotenv
from log_config import setup_logging
from datetime import datetime

logger = setup_logging("search_info_fiis")
dotenv.load_dotenv()
keyApi = os.getenv('API_TOKEN')
preco_alvo = float(os.getenv('PRICE_SEARCH', 5))  # Valor alvo para o preço das ações

try:
    with open("alvos.csv", "r", encoding="utf-8") as f:
        tickets = csv.reader(f)
        tickets = [row[0] for row in tickets if row]  # Extrai apenas os tickers
except FileNotFoundError:
    logger.error("Arquivo 'alvos.csv' nao encontrado.")


try:
    bot = TelegramBot()
    logger.info("Iniciando busca das ações")


    for tick in tickets:
        Ticker = yf.Ticker(tick)
        hist = Ticker.history(period="1mo", interval="1d")
        info = Ticker.info
        Price = info.get("regularMarketPrice")
        # n = info.get("lastDividendValue")
        # d = info.get("lastDividendDate")
        # r = info.get("dividendRate")
        # di = datetime.fromtimestamp(d).strftime("%d-%m-%Y")
        # dividendos = Ticker.dividends

        dayOpen = info.get("open")
        daylow = info.get("dayLow")
        dayhigh = info.get("dayHigh")   

        bot.send_message(f'{tick} - Preço atual: R${Price}, Abertura: {dayOpen}, Mínimo {daylow}, Máximo: {dayhigh} \n')
   
except Exception as e:
        bot.send_message(f"Erro ao obter informações da ação: {Ticker}\n Detalhes do erro: {e}")
        logger.error(f"Erro ao obter informações da ação: {Ticker}\n Detalhes do erro: {e}")