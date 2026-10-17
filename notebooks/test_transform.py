import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transform import transform_dataframe

def pipeline():
    records = [
        {
            "cotacaoCompra": 4.9692,
            "cotacaoVenda": 0,
            "dataHoraCotacao": "2026-10-06 13:03:21.267287"
        }
    ]
    
    df = transform_dataframe(records)

pipeline()