import pandas as pd
import numpy as np
from pathlib import Path

base = Path("/home/gabriel/Projetos/Data Science/PAS/diagnosticos")

trienios = [
    "2018-2020", "2019-2021", "2020-2022",
    "2021-2023", "2022-2024", "2023-2025",
]
posicao = {t: i for i, t in enumerate(trienios)}  # 0 a 5, ordem no tempo

dfs = []
for t in trienios:
    df = pd.read_csv(base / f"{t}.csv")
    df["trienio"] = t
    dfs.append(df)
todos = pd.concat(dfs, ignore_index=True)

chave = ["Curso", "Campus", "Turno", "modalidade_normalizada"]

def calcular_grupo(g):
    g = g.sort_values("trienio", key=lambda s: s.map(posicao))
    posicoes = g["trienio"].map(posicao).to_numpy()
    notas = g["Nota Mínima"].to_numpy()  # nota mínima = nota de corte
    n = len(g)
    primeiro_trienio, ultimo_trienio = g["trienio"].iloc[0], g["trienio"].iloc[-1]
    variacao_absoluta = notas[-1] - notas[0]
    slope = np.polyfit(posicoes, notas, 1)[0] if n >= 2 else np.nan
    cobre_inicio = primeiro_trienio in ("2018-2020", "2019-2021")
    cobre_fim = ultimo_trienio in ("2022-2024", "2023-2025")
    elegivel = (n >= 4) and cobre_inicio and cobre_fim
    return pd.Series({
        "n_trienios": n,
        "primeiro_trienio": primeiro_trienio,
        "ultimo_trienio": ultimo_trienio,
        "variacao_absoluta": variacao_absoluta,
        "slope": slope,
        "elegivel_ranking_principal": elegivel,
    })

tendencias = todos.groupby(chave).apply(calcular_grupo).reset_index()

principal = tendencias[tendencias["elegivel_ranking_principal"]].sort_values("slope", ascending=False)
suplementar = tendencias[~tendencias["elegivel_ranking_principal"]].sort_values("slope", ascending=False)

principal.to_csv(base / "tendencia_ranking_principal.csv", index=False)
suplementar.to_csv(base / "tendencia_tabela_suplementar.csv", index=False)

print(f"Ranking principal: {len(principal)} combinações")
print(f"Tabela suplementar: {len(suplementar)} combinações")
print(principal.head(10).to_string())

# Headline oficial (ampla concorrência) para o corpo do artigo.
# AC é o grupo mais numeroso/estável; cotas específicas ficam como camada
# secundária/exploratória (equidade de acesso), não para ranking de tendência.
headline = principal[principal["modalidade_normalizada"] == "AC"].sort_values("slope", ascending=False)
headline.to_csv(base / "tendencia_headline_AC.csv", index=False)
print(f"Headline (AC): {len(headline)} combinações curso/campus/turno")
print(headline.head(10).to_string())
