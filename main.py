from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import text
from datetime import datetime, timedelta, date

from src.extract import extract_cotacao
from src.transform import transform_dataframe
from src.load import load_data

from src.load import get_engine

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent / 'config' / '.env'
load_dotenv(env_path)

engine = get_engine()

table = os.getenv('DB_TABLE')
schema = os.getenv('DB_SCHEMA')

def extract_date():
    query = text(f"SELECT MAX(data_hora) FROM {schema}.{table};")

    with engine.connect() as conn:
        ultima = conn.execute(query).scalar()

    if ultima is not None:
        if isinstance(ultima, str):
            ultima = datetime.strptime(ultima.split('.')[0], "%Y-%m-%d %H:%M:%S")
        proxima = ultima.date() + timedelta(days=1)

    else:
        proxima = datetime.strptime("10-01-2026", "%m-%d-%Y").date()

    # data_formatada = proxima.strftime("%m-%d-%Y")

    return proxima

data_inicio = extract_date()
hoje = date.today()
data_final = hoje


url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{data_inicio.strftime("%m-%d-%Y")}'&@dataFinalCotacao='{data_final.strftime("%m-%d-%Y")}'&$top=100&$format=json"

print(f"A data que deve buscar é entre {data_inicio} e {data_final}")

def pipeline():
    try:
        if data_inicio > data_final:
            logging.info("Data inválida!")
            return

        logging.info("ETAPA 1: EXTRAÇÃO")
        records = extract_cotacao(url)

        if records == []:
            logging.info("Pipeline finalizado sem novos dados!")
            return

        logging.info("ETAPA 2: TRANSFORMAÇÃO")
        df = transform_dataframe(records)

        logging.info('ETAPA 3: CARREGAMENTO')
        load_data(table, schema, df)

        print("\n" + "="*60)
        print("Pipeline concluído com sucesso!")
        print("="*60)

    except Exception as e:
        logging.error(f"Erro no pipeline: {e}")
        raise

pipeline()