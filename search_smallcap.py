import yfinance as yf
import os
from telegrambot import TelegramBot
import dotenv
from log_config import setup_logging
from datetime import datetime, timedelta


logger = setup_logging("seach_smallcap")
dotenv.load_dotenv()

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

def calcular_aumento_percentual(valor_inicial: float, valor_final: float) -> float:
    if valor_inicial == 0:
        raise ValueError("O valor inicial não pode ser zero.")

    aumento = ((valor_final - valor_inicial) / valor_inicial) * 100
    return round(aumento, 2)

try:
    bot = TelegramBot(token_env="BOT_TOKEN_PYTHON_SEARCH", chat_id_env="CHAT_ID_SMALLCAP")
    mensagem = ""
    tickets = [
    "Alpa3.SA",
    "Anim3.SA",
    "Axia3.SA",
    "B3sa3.SA",
    "Bbse3.SA",
    "Bmgb4.SA",
    "Cmig4.SA",
    "Cogn3.SA",
    "Cple3.SA",
    "Csna3.SA",
    "Cxse3.SA",
    "Egie3.SA",
    "Engi4.SA",
    "Fesa4.SA",
    "Grnd3.SA",
    "Itsa4.SA",
    "Jslg3.SA",
    "Lavv3.SA",
    "Mdne3.SA",
    "Melk3.SA",
    "Mglu3.SA",
    "Mrve3.SA",
    "Mtre3.SA",
    "Pgmn3.SA",
    "Pomo3.SA",
    "Pomo4.SA",
    "Rail3.SA",
    "Recv3.SA",
    "Rdor3.SA",
    "Sapr4.SA",
    "Vamo3.SA"
]


    for tick in tickets:
        Ticker = yf.Ticker(tick)
        info = Ticker.info

        Price = info.get("regularMarketPrice")
        dayOpen = info.get("open")
        daylow = info.get("dayLow")
        dayhigh = info.get("dayHigh")

        # lastDividendValue = info.get("lastDividendValue")
        # exDividendTimestamp = info.get("exDividendDate")  # <<< usamos ex-dividend date

        dividendRate = info.get("dividendRate")
        dividendYield = info.get("dividendYield")

          # Calcular yield do último pagamento
        yield_ultimo = None
        preco_ref = None
        exDividendDateFmt = None

        # if lastDividendValue and exDividendTimestamp:
        #     exDividendDate = datetime.fromtimestamp(exDividendTimestamp)
        #     exDividendDateFmt = exDividendDate.strftime("%d/%m/%Y")

            # preço do dia COM (fechamento anterior ao ex-dividend date)
            # preco_ref = get_preco_referencia(Ticker, exDividendTimestamp)
            # if preco_ref:
            #     yield_ultimo = (lastDividendValue / preco_ref) * 100

        # 1. Definir o primeiro dia do mês atual
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1).strftime('%Y-%m-%d')

        # 2. Buscar histórico do dia 1 até hoje
        hist_mes = Ticker.history(start=inicio_mes)

        # 3. Calcular Máxima e Mínima do dataframe retornado
        if not hist_mes.empty:
            # Pega o maior valor da coluna 'High' e o menor da 'Low'
            max_mes = hist_mes['High'].max()
            data_max = hist_mes['High'].idxmax().strftime('%d/%m')
            min_mes = hist_mes['Low'].min()
            data_min = hist_mes['Low'].idxmin().strftime('%d/%m')
        else:
            # Fallback caso seja o primeiro dia do mês e mercado não abriu
            max_mes = dayhigh
            min_mes = daylow
            data_min ='01-01'
            data_max ='01-01'




        aumento_percentual_dia = calcular_aumento_percentual(daylow, dayhigh)
        aumento_percentual_mes= calcular_aumento_percentual(min_mes, max_mes)
        
        mensagem += (
                    f"📈 {tick}\n"
                    f"💰 Preço Atual: R$ {Price}\n"
                    f"🔓 Abertura: R$ {dayOpen}\n"
                    f"⬇️ Mínimo Dia: R$ {daylow}\n"
                    f"⬆️ Máximo Dia: R$ {dayhigh}\n"
                    f"Aumento percentual dia: {aumento_percentual_dia}%\n"
                    f"📉 Mínima Mês: R$ {min_mes:.2f} ({data_min})\n"
                    f"📈 Máxima Mês: R$ {max_mes:.2f} ({data_max})\n"
                    f"Aumento percentual mês: {aumento_percentual_mes}%\n"
                    # f"💲 Último Dividendo: R$ {lastDividendValue}\n"
                    # f"📆 Data Ex-Dividendo: {exDividendDateFmt}\n"
                )

        mensagem += "-------------------------\n"

        print(mensagem)
        bot.send_message(mensagem)

except Exception as e:
    bot.send_message(f"Erro ao obter informações da ação: {tick}\n Detalhes do erro: {e}")
    logger.error(f"Erro ao obter informações da ação: {tick}\n Detalhes do erro: {e}")
