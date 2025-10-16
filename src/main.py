import os
import pandas as pd
from ingestion import load_and_merge
from cleaning import limpar_dados
from features import criar_features
from analysis import (
    contagem_por_ano,
    contagem_por_mes
)

def _print_df(titulo: str, df: pd.DataFrame, max_rows: int = 12):
    """Imprime um DataFrame com título e número limitado de linhas."""
    print("\n===", titulo, "===")
    linhas = len(df)
    if linhas == 0:
        print("(sem linhas)")
        return
    if linhas > max_rows:
        print(df.head(max_rows).to_string(index=False))
        print(f"... ({linhas - max_rows} linhas adicionais ocultas)")
    else:
        print(df.to_string(index=False))
    print(f"Total de linhas exibidas/armazenadas: {linhas}")

def main():
    # --- 1. Ingestion ---
    df = load_and_merge(
        dados_path="raw_data/DADOS_MG",
        output_path="processed_data/focos_merged.csv"
    )

    # --- 2. Cleaning ---
    df = limpar_dados(df)

    # --- 3. Features ---
    df = criar_features(df)

    # --- 4. Análise / Exportação CSVs ---
    output_dir = "processed_data/"
    os.makedirs(output_dir, exist_ok=True)

    parametros = {
        'ranking_top_k': 10
    }

    df_por_ano = contagem_por_ano(df)
    df_por_mes = contagem_por_mes(df)


    # Exporta CSVs
    df_por_ano.to_csv(os.path.join(output_dir, "contagem_por_ano.csv"), index=False)
    df_por_mes.to_csv(os.path.join(output_dir, "contagem_por_mes.csv"), index=False)

    print("Pipeline completo. CSVs gerados em:", output_dir)
    print("Total de linhas no dataset final:", len(df))
    print("Parâmetros usados:")
    for k,v in parametros.items():
        print(f"  - {k} = {v}")

    # Impressões legíveis dos resultados
    _print_df("Contagem por Ano", df_por_ano)
    _print_df("Contagem por Mês", df_por_mes)

if __name__ == "__main__":
    main()