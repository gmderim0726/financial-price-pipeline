import pandas as pd

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

columns_rename = {
                'cotacaoCompra': 'cotacao_compra',
                'cotacaoVenda': 'cotacao_venda',
                'dataHoraCotacao': 'data_hora',
                }

def create_dataframe(records:list) -> pd.DataFrame:
    logging.info(f"Criado DataFrame da API...")
    df = pd.json_normalize(records)
    logging.info(f"Dataframe criado com {len(df)} linha(s)")
    return df

def convert_type(df:pd.DataFrame) -> pd.DataFrame:
    logging.info(f"Convertendo colunas para datetime...")
    df['dataHoraCotacao'] = pd.to_datetime(df['dataHoraCotacao'])
    logging.info(f"Coluna convertida")
    return df

def rename_columns(df:pd.DataFrame, columns_name:dict[str, str]) -> pd.DataFrame:
    logging.info(f"Renomeando {len(columns_name)} colunas...")
    df = df.rename(columns=columns_name)
    logging.info(f"Colunas renomeadas")
    return df

def null_values(df:pd.DataFrame) -> pd.DataFrame:
    logging.info("Verificando a existência de valores nulos...")
    if df.isna().any().any():
        raise ValueError("O dado não pode ser nulo!")
    return df

def plus_values(df:pd.DataFrame) -> pd.DataFrame:
    logging.info("Validando valores positivos das cotações...")
    if (df[['cotacao_compra','cotacao_venda']]<= 0).any().any():
        raise ValueError("As cotações devem ser maiores que zero!")
    return df

def transform_dataframe(records):
    logging.info("Iniciando transformações")
    df = create_dataframe(records)
    df = convert_type(df)
    df = rename_columns(df, columns_rename)
    df = null_values(df)
    df = plus_values(df)
    logging.info("Transformações concluídas")
    return df

# if __name__ == "__main__":
#     df = transform_dataframe()
#     tipos = df.dtypes
#     nulos = df.isna().sum()
#     print(df)
#     print(tipos)
#     print(nulos)