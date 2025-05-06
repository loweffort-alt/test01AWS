import pandas as pd


def leer_csv(ruta_archivo):
    # Leer el archivo CSV
    df = pd.read_csv(ruta_archivo)
    return df
