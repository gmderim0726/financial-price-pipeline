import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
table = os.getenv('DB_TABLE')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
schema = os.getenv('DB_SCHEMA')

def get_engine():
    logging.info(f"Conectando em {host}:{port}/{database}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )

engine = get_engine()

def conflict_nothing(table_class, conn, keys, data_iter):
    metadata = MetaData()
    table = Table(table_class.name, metadata, schema=table_class.schema, autoload_with=conn.engine)

    data = [dict(zip(keys,row)) for row in data_iter]

    stmt = insert(table).values(data)

    stmt_seguro = stmt.on_conflict_do_nothing(index_elements=['data_hora'])

    conn.execute(stmt_seguro)

def load_data(table_name:str, schema_name:str, df:pd.DataFrame):
    df.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append', index=False, method=conflict_nothing)
    logging.info(f"Dados carregados com sucesso! \n")

    df_check = pd.read_sql(f'SELECT * FROM {schema_name}.{table_name}', con=engine)
    logging.info(f"Total de registros na tabela: {len(df_check)}\n")