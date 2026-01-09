import yfinance as yf
import os
from telegrambot import TelegramBot
import dotenv
from log_config import setup_logging
from datetime import datetime, timedelta

logger = setup_logging("search_info_fiis")
dotenv.load_dotenv()
keyApi = os.getenv('API_TOKEN')
preco_alvo = float(os.getenv('PRICE_SEARCH', 5))  # Valor alvo para o preço das ações


def format_date(timestamp):
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")


def get_preco_referencia(ticker, ex_dividend_timestamp):
    """
    Busca o preço de fechamento do último pregão antes da data ex-dividendo.
    Se cair em final de semana/feriado, volta até 7 dias atrás.
    """
    dia = datetime.fromtimestamp(ex_dividend_timestamp) - timedelta(days=1)

    for _ in range(7):  # tenta até 7 dias para trás
        hist = ticker.history(
            start=dia.strftime("%Y-%m-%d"),
            end=(dia + timedelta(days=1)).strftime("%Y-%m-%d")
        )
        if not hist.empty:
            return hist["Close"].iloc[-1]

        dia -= timedelta(days=1)  # tenta o dia anterior

    return None  # se não achou nada


try:
    bot = TelegramBot()
    mensagem = ""
    tickets = ["VGIR11.SA","PETR4.SA","VGRI11.SA"]

    for tick in tickets:
        Ticker = yf.Ticker(tick)
        info = Ticker.info

        Price = info.get("regularMarketPrice")
        dayOpen = info.get("open")
        daylow = info.get("dayLow")
        dayhigh = info.get("dayHigh")

        lastDividendValue = info.get("lastDividendValue")
        exDividendTimestamp = info.get("exDividendDate")  # <<< usamos ex-dividend date

        dividendRate = info.get("dividendRate")
        dividendYield = info.get("dividendYield")

        # Calcular yield do último pagamento
        yield_ultimo = None
        preco_ref = None
        exDividendDateFmt = None

        if lastDividendValue and exDividendTimestamp:
            exDividendDate = datetime.fromtimestamp(exDividendTimestamp)
            exDividendDateFmt = exDividendDate.strftime("%d/%m/%Y")

            # preço do dia COM (fechamento anterior ao ex-dividend date)
            preco_ref = get_preco_referencia(Ticker, exDividendTimestamp)
            if preco_ref:
                yield_ultimo = (lastDividendValue / preco_ref) * 100

        mensagem += (
            f"📈 {tick}\n"
            f"💰 Preço Atual: R$ {Price}\n"
            f"🔓 Abertura: R$ {dayOpen}\n"
            f"⬇️ Mínimo: R$ {daylow}\n"
            f"⬆️ Máximo: R$ {dayhigh}\n"
            f"📉 Último Dividendo: R$ {lastDividendValue}\n"
            f"📆 Data Ex-Dividendo: {exDividendDateFmt}\n"
        )

        if preco_ref:
            mensagem += (
                f"📊 Preço Ref. (fechamento no dia COM): R$ {preco_ref:.2f}\n"
                f"📈 Yield do Último Pagamento: {yield_ultimo:.2f}%\n"
            )

        mensagem += "-------------------------\n"

    print(mensagem)
    bot.send_message(mensagem)

except Exception as e:
    bot.send_message(f"Erro ao obter informações da ação: {tick}\n Detalhes do erro: {e}")
    logger.error(f"Erro ao obter informações da ação: {tick}\n Detalhes do erro: {e}")
