from pathlib import Path

import pandas as pd
import tabula


def convert_data(filename):
    dfs = tabula.read_pdf(f"data/raw/{filename}.pdf", pages="all")
    df = pd.concat(dfs)
    df.to_parquet(f"data/converted/{filename}.pq")


def clean_data(filename):
    df = pd.read_parquet(f"data/converted/{filename}.pq")
    df.rename(
        columns={
            "Dato": "date",
            "Posteringstekst": "text",
            "Overførsel": "source",
            "Beløb": "amount",
            "Saldo": "balance",
            "Valuta": "currency",
        },
        inplace=True,
    )
    df["date"] = pd.to_datetime(df["date"], format=r"%d/%m/%Y")

    df["amount"] = pd.to_numeric(
        df["amount"].str.replace(".", "").str.replace(",", ".")
    )
    df["balance"] = pd.to_numeric(
        df["balance"].str.replace(".", "").str.replace(",", ".")
    )

    df.to_parquet(f"data/clean/{filename}.pq")


def attach_categories(df_in):
    df = df_in.copy()
    # each new column, or one common dictionary column ?
    df["category"] = None
    df["location"] = None
    for index, row in df.iterrows():

        if "REMA 1000" in row["text"]:
            category = "Dagligvarer"
            df.loc[index, "category"] = category
        if "valby" in row["text"].lower():
            location = "Valby"
            df.loc[index, "location"] = location
    return df


def process_data(filename):
    convert_data(filename)
    clean_data(filename)


def read_clean(filename):
    full_path = f"data/clean/{filename}.pq"
    file = Path(filename)
    if not file.is_file():
        process_data(filename)
    df = pd.read_parquet(full_path)
    return df
