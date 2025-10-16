import pandas as pd

def aplicar_filtros(
    df: pd.DataFrame,
    ano_inicio: int = None,
    ano_fim: int = None,
    meses: list = None,
    estacoes: list = None,
    biomas: list = None,
    municipios: list = None
) -> pd.DataFrame:
    """Filtra o DataFrame por parâmetros opcionais."""
    df_filtro = df.copy()
    if ano_inicio is not None:
        df_filtro = df_filtro[df_filtro['ano'] >= ano_inicio]
    if ano_fim is not None:
        df_filtro = df_filtro[df_filtro['ano'] <= ano_fim]
    if meses is not None:
        df_filtro = df_filtro[df_filtro['mes'].isin(meses)]
    if estacoes is not None:
        df_filtro = df_filtro[df_filtro['estacao'].isin(estacoes)]
    if biomas is not None:
        df_filtro = df_filtro[df_filtro['bioma'].isin(biomas)]
    if municipios is not None:
        df_filtro = df_filtro[df_filtro['municipio'].isin([m.upper() for m in municipios])]
    return df_filtro

def contagem_por_ano(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby('ano').size().reset_index(name='total_focos')
    return result.sort_values('ano')

def contagem_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby('mes').size().reset_index(name='total_focos')
    return result.sort_values('mes')

# def tendencia_geral(df: pd.DataFrame) -> float:
#     cont = contagem_por_ano(df)
#     if len(cont) < 2:
#         return 0.0
#     inicial = cont.iloc[0]['total_focos']
#     final = cont.iloc[-1]['total_focos']
#     if inicial == 0:
#         return 0.0
#     return ((final - inicial) / inicial) * 100
