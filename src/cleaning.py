import pandas as pd

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Limpeza e padronização do dataset.

    Etapas:
    - Remove duplicados
    - Converte coluna de data ('data_pas')
    - Padroniza colunas de string (municipio/bioma/estado)
    - Remove linhas com datas inválidas
    """
    df = df.drop_duplicates()
    df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')
    if 'municipio' in df.columns:
        df['municipio'] = df['municipio'].astype(str).str.strip().str.upper()
    if 'bioma' in df.columns:
        df['bioma'] = df['bioma'].astype(str).str.strip().str.capitalize()
    if 'estado' in df.columns:
        df['estado'] = df['estado'].astype(str).str.strip().str.upper()
    df = df[df['data_pas'].notnull()]
    return df
