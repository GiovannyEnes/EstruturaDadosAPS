# Pipeline de Focos de Queimadas (MG)

Pipeline simples para carregar diversos arquivos CSV anuais de focos de queimadas em Minas Gerais, limpar, criar colunas derivadas e gerar estatísticas agregadas.

## Estrutura
```
raw_data/
  DADOS_MG/              # CSVs anuais: focos_br_mg_ref_YYYY.csv
processed_data/          # Saída: dataset mesclado e agregações
src/
  ingestion.py           # Carregamento e merge incremental
  cleaning.py            # Limpeza básica (limpar_dados)
  features.py            # Criação de features (criar_features)
  analysis.py            # Funções de análise agregada
  main.py                # Orquestra o pipeline
```

## Etapas
1. Ingestion: une todos os anos (incremental se já existir arquivo).
2. Cleaning: remove duplicados, corrige datas e padroniza strings.
3. Features: adiciona `ano`, `mes`, `estacao`.
4. Analysis: gera contagens por ano, mês, estação, município e bioma.

## Uso
Executar pipeline completo:
```bash
python src/main.py
```
PowerShell:
```powershell
python .\src\main.py
```

Forçar reconstrução completa:
```powershell
python -c "from src.ingestion import load_and_merge; df = load_and_merge(force_rebuild=True); print(len(df))"
```

## Saídas principais
- processed_data/focos_merged.csv
- processed_data/contagem_por_ano.csv
- processed_data/contagem_por_mes.csv

## Melhorias Futuras
- Adicionar testes automatizados
- CLI com parâmetros (anos, filtro de municípios)
- Documentar formato das colunas

## Licença
MIT
