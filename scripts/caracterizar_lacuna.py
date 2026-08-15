import pandas as pd
from pathlib import Path

# ajuste este caminho se a pasta do projeto não for exatamente essa
base = Path("/home/gabriel/Projetos/Data Science/PAS/diagnosticos")

trienios = [
    "2018-2020", "2019-2021", "2020-2022",
    "2021-2023", "2022-2024", "2023-2025",
]

dfs = []
for t in trienios:
    df = pd.read_csv(base / f"{t}.csv")
    df["trienio"] = t
    dfs.append(df)

todos = pd.concat(dfs, ignore_index=True)

# chave que define uma "série" comparável ao longo do tempo
chave = ["Curso", "Campus", "Turno", "modalidade_normalizada"]

# em quantos triênios cada combinação aparece
presenca = (
    todos.groupby(chave)["trienio"].nunique().reset_index(name="n_trienios")
)
presenca.to_csv(base / "presenca_por_combinacao.csv", index=False)

# combinações que existem nos outros 5 triênios mas não aparecem em 2022-2024
chaves_outros = set(
    todos[todos["trienio"] != "2022-2024"].groupby(chave).groups.keys()
)
chaves_2022_2024 = set(
    todos[todos["trienio"] == "2022-2024"].groupby(chave).groups.keys()
)
ausentes = chaves_outros - chaves_2022_2024

print(f"Combinações presentes em algum dos outros 5 triênios: {len(chaves_outros)}")
print(f"Combinações presentes em 2022-2024: {len(chaves_2022_2024)}")
print(f"Combinações ausentes em 2022-2024: {len(ausentes)}")

pd.DataFrame(list(ausentes), columns=chave).to_csv(
    base / "ausentes_2022_2024.csv", index=False
)
