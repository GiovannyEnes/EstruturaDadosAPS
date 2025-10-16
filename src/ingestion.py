import pandas as pd
import glob
import os

def _ano_arquivo(caminho: str) -> int:
    """Extrai o ano do nome do arquivo assumindo padrão *_YYYY.csv"""
    base = os.path.basename(caminho)
    try:
        return int(base.split('_')[-1].split('.')[0])
    except (ValueError, IndexError):
        raise ValueError(f"Nome de arquivo não segue padrão esperado para ano: {base}")

def load_and_merge(dados_path: str = "raw_data/DADOS_MG",
                   output_path: str = "processed_data/focos_merged.csv",
                   force_rebuild: bool = False) -> pd.DataFrame:
    """Carrega todos os CSVs anuais, detecta novos anos, faz merge incremental ou reconstrução completa e salva CSV final.

    Parâmetros
    ----------
    dados_path : str
        Diretório contendo os arquivos CSV anuais.
    output_path : str
        Caminho para o CSV mesclado final.
    force_rebuild : bool
        Se True, força reconstrução completa mesmo se já existir arquivo.
    """

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not os.path.isabs(dados_path):
        dados_path = os.path.join(project_root, dados_path)
    if not os.path.isabs(output_path):
        output_path = os.path.join(project_root, output_path)

    csvs = glob.glob(os.path.join(dados_path, "*.csv"))
    if not csvs:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {dados_path}")
    print(f"{len(csvs)} arquivos encontrados em {dados_path}")

    anos_arquivos = [_ano_arquivo(f) for f in csvs]
    if os.path.exists(output_path):
        df_existente = pd.read_csv(output_path)
        if 'data_pas' not in df_existente.columns:
            raise ValueError("Arquivo existente não contém coluna 'data_pas'.")
        df_existente['data_pas'] = pd.to_datetime(df_existente['data_pas'], errors='coerce')
        df_existente['ano'] = df_existente['data_pas'].dt.year
        anos_existentes = df_existente['ano'].dropna().unique().tolist()
        novos_anos = [a for a in anos_arquivos if a not in anos_existentes]
        if not novos_anos:
            print("Nenhum ano novo encontrado. Retornando dataset existente.")
            return df_existente
        else:
            print(f"Novos anos detectados: {novos_anos}")
    else:
        novos_anos = anos_arquivos

    if os.path.exists(output_path) and not force_rebuild:
        df_existente = pd.read_csv(output_path)
        csvs_novos = [f for f in csvs if _ano_arquivo(f) in novos_anos]
        if csvs_novos:
            dfs_novos = [pd.read_csv(f) for f in csvs_novos]
            df_novos = pd.concat(dfs_novos, ignore_index=True)
            df_merged = pd.concat([df_existente, df_novos], ignore_index=True)
            print(f"Foram adicionadas {len(df_novos)} linhas de {len(csvs_novos)} arquivos novos.")
        else:
            print("Nenhum arquivo novo para adicionar. Retornando existente.")
            return df_existente
    else:
        dfs = [pd.read_csv(f) for f in csvs]
        df_merged = pd.concat(dfs, ignore_index=True)
        if force_rebuild:
            print("Reconstrução completa solicitada (force_rebuild=True).")

    df_merged['data_pas'] = pd.to_datetime(df_merged['data_pas'], errors='coerce')
    if 'municipio' in df_merged.columns:
        df_merged['municipio'] = df_merged['municipio'].astype(str).str.strip().str.upper()
    if 'bioma' in df_merged.columns:
        df_merged['bioma'] = df_merged['bioma'].astype(str).str.strip().str.capitalize()
    if 'estado' in df_merged.columns:
        df_merged['estado'] = df_merged['estado'].astype(str).str.strip().str.upper()

    df_merged.drop_duplicates(inplace=True)
    df_merged = df_merged.sort_values('data_pas').reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_merged.to_csv(output_path, index=False)
    print(f"CSV final salvo em: {output_path}")

    return df_merged


if __name__ == "__main__":
    df_final = load_and_merge()
    print("Merge completo. Linhas totais:", len(df_final))
