import yfinance as yf
import json
import csv
import os
from telegrambot import TelegramBot
import dotenv
from log_config import setup_logging

logger = setup_logging("main")
dotenv.load_dotenv()
keyApi = os.getenv('API_TOKEN')
preco_alvo = int(os.getenv('PRICE_SEARCH', 5))  # Valor alvo para o preço das ações
acoes_abaixo_10_json = {}
acoes_abaixo_10_csv = []

try:
    with open("acoes.csv", "r", encoding="utf-8") as f:
        tickets = csv.reader(f)
        tickets = [row[0] for row in tickets if row]  # Extrai apenas os tickers
except FileNotFoundError:
    print("Arquivo 'acoes.csv' nao encontrado.")
    logger.error("Arquivo 'acoes.csv' nao encontrado.")


try:
    bot = TelegramBot()
    print("Iniciando busca das ações")
    logger.info("Iniciando busca das ações")

    for tick in tickets:
        Ticker = yf.Ticker(tick)  # Adiciona .SA para ações brasileiras
        hist = Ticker.history(period="1mo", interval="1d")
        info = Ticker.info
        Price = info.get("regularMarketPrice")
        if Price is None:
            logger.error(f"Preço não encontrado para o ticker: {tick}")
            continue
        if isinstance(Price, (int, float)) and (Price <= preco_alvo or tick == "PETR4.SA"):
       
            msg = f'Ticker: {tick} Preço atual R$:{Price} \n'
            # print(msg)
            acoes_abaixo_10_json[tick] = Price
            # bot.send_message(f' Ticker: {tick} Preço atual R$:{Price} \n')
            
            # Adiciona os dados ao arquivo json
            with open("acoes_abaixo_10.json", "w", encoding="utf-8") as f:
                json.dump(acoes_abaixo_10_json, f, ensure_ascii=False, indent=4)

            # Adiciona os dados ao arquivo csv
            acoes_abaixo_10_csv.append((tick, Price))
            with open("acoes_abaixo_10.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # writer.writerow(["ticker", "preco"])  # cabeçalho
                writer.writerows(acoes_abaixo_10_csv)

        # else:
        #     print(f' Ticker: {tick}  Preço atual R$: {Price} \n')
    logger.info(f"Tickets abaixo de R${preco_alvo} adicionados aos arquivos JSON e CSV")
    logger.info("Busca das ações concluida")
except Exception as e:
            #  print(f"Erro ao obter informações da ação: {Ticker}\n Detalhes do erro: {e}")
             logger.error(f"Erro ao obter informações da ação: {Ticker} \n Detalhes do erro: {e}")
            #  bot.send_message(f"Erro ao obter informações da ação: {Ticker}\nDetalhes do erro: {e}")
