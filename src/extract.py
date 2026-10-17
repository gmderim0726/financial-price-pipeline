import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_cotacao(url:str) -> list:
    try:
        response = requests.get(url, timeout=(5,20))
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logging.error('A requisição excedeu tempo limite!')
        raise 
    except requests.exceptions.RequestException as e:
        logging.error(f"Outro erro na requisição: {e}")
        raise
        
    if response.status_code != 200:
        logging.error("Erro na requisição")
        return []

    data = response.json()
    if not data['value']:
        logging.warning("Nenhum dado retornado")
        return []

    output_path = Path(__file__).parent.parent/'data'/'cotacao.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Arquivo salvo em {output_path}")
    return data['value']