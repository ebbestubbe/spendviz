import pandas as pd

import tabula


def convert_data(filename):
    dfs = tabula.read_pdf(f"data/raw/{filename}.pdf", pages='all')
    df = pd.concat(dfs)
    df.to_parquet(f'data/converted/{filename}.pq')

def clean_data(filename):
    df = pd.read_parquet(f'data/converted/{filename}.pq')
    df.rename(
        columns={
            "Dato": "date",
            "Overførsel": "source",
            "Beløb": "amount",
            "Saldo": "balance",
            "Valuta": "currency"
        },
        inplace=True
    )
    df['date'] = pd.to_datetime(df['date'])
    
    df['amount'] = pd.to_numeric(df['amount'].str.replace('.','').str.replace(',','.'))
    df['balance'] = pd.to_numeric(df['balance'].str.replace('.','').str.replace(',','.'))
    df.to_parquet(f'data/clean/{filename}.pq')

def process_data(filename):
    convert_data(filename)
    clean_data(filename)

def read_clean(filename):
    df = pd.read_parquet(f'data/clean/{filename}.pq')
    return df