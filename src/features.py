import pandas as pd

def estacao_do_ano(mes: int) -> str:
    if mes in [12, 1, 2]:
        return "Verão"
    elif mes in [3, 4, 5]:
        return "Outono"
    elif mes in [6, 7, 8]:
        return "Inverno"
    else:
        return "Primavera"

def criar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas derivadas: ano, mês, estação."""
    df['ano'] = df['data_pas'].dt.year
    df['mes'] = df['data_pas'].dt.month
    df['estacao'] = df['mes'].apply(estacao_do_ano)
    return df
