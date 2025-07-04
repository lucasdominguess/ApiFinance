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
    print("Arquivo 'alvos.csv' nao encontrado.")
    logger.error("Arquivo 'alvos.csv' nao encontrado.")


try:
    bot = TelegramBot()
    print("Iniciando busca das ações")
    logger.info("Iniciando busca das ações")


    for tick in tickets:
        Ticker = yf.Ticker(tick)
        hist = Ticker.history(period="1mo", interval="1d")
        info = Ticker.info
        Price = info.get("regularMarketPrice")
        dividendos = Ticker.dividends
        if not dividendos.empty:
            ultimo_pagamento_valor = dividendos.iloc[-1]
            ultimo_pagamento_data = dividendos.index[-1].strftime("%Y-%m-%d")
        else:
            ultimo_pagamento_valor = None
            ultimo_pagamento_data = None

        ex_dividend_ts = Ticker.info.get("exDividendDate")
        ex_dividend_data = datetime.fromtimestamp(ex_dividend_ts).strftime("%d-%m-%Y") if ex_dividend_ts else None

        dy = Ticker.info.get("dividendYield")
        dy_percent = round(dy if dy > 1 else dy * 100, 2)

        # print("Último pagamento:", ultimo_pagamento_valor, "em", ultimo_pagamento_data)
        # print("Próxima data com:", ex_dividend_data)
        # print("Dividend Yield:", dy_percent, "%")

        bot.send_message(f'Ticker: {tick} Preço atual R$:{Price} \n'
                                        f'Último pagamento: R${ultimo_pagamento_valor} em {ultimo_pagamento_data}\n'
                                        f'Próxima data com: {ex_dividend_data}\n'
                                        f'Dividend Yield: {dy_percent}%')
except Exception as e:
        print(f"Erro ao obter informações da ação: {Ticker}\n Detalhes do erro: {e}")
        logger.error(f"Erro ao obter informações da ação: {Ticker}\n Detalhes do erro: {e}")