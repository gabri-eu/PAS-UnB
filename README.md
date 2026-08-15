# PAS UnB — Análise de Notas de Corte e Tendências

Projeto de análise dos dados do **Programa de Avaliação Seriada (PAS)** da Universidade de Brasília (UnB): notas de corte por curso, campus, turno e modalidade de cota ao longo dos triênios 2018-2020 a 2023-2025, com foco em identificar **cursos com tendência de crescimento de demanda**.

> Nota: as "notas" aqui são **escore do PAS** (próprio do processo seriado da UnB), não nota do ENEM. Correlação com ENEM/SISU está prevista como etapa futura, ainda sem dados.

## Estrutura

```text
PAS/
├── 00_catalogo_historico.ipynb … 05_inteligencia_analitica.ipynb
├── 99_auditoria_artefatos.ipynb
├── scripts/
│   ├── caracterizar_lacuna.py          # diagnóstico da cobertura por triênio
│   └── calcular_tendencia.py           # slope/variação por combinação (painel desbalanceado)
├── diagnosticos/                      # CSVs limpos por triênio + resumos + saídas de tendência
│   ├── tendencia_headline_AC.csv      # ★ lista oficial (ampla concorrência) p/ o artigo
│   ├── tendencia_ranking_principal.csv# todas as modalidades (material suplementar/cotas)
│   └── tendencia_tabela_suplementar.csv
├── estatisticas/  normalizado/  catalogos/  relatorios/  tsv/
├── docs/RESUMO_ESTADO_PROJETO.md
└── README.md
```

## Pipeline de tendência

1. **`scripts/caracterizar_lacuna.py`** — conta em quantos triênios cada combinação
   (Curso × Campus × Turno × modalidade) aparece. Gera `presenca_por_combinacao.csv`
   e `ausentes_2022_2024.csv`.
2. **`scripts/calcular_tendencia.py`** — regressão linear (slope) e variação absoluta da
   nota de corte por combinação, respeitando critério de elegibilidade:
   - `n_trienios >= 4`
   - cobre pelo menos um ponto no **início** (2018-2020 ou 2019-2021) **e** um no **fim** (2022-2024 ou 2023-2025)
   - métrica principal = **AC (ampla concorrência)** → `tendencia_headline_AC.csv`

## Como rodar

```bash
cd PAS
source .venv/bin/activate
python scripts/caracterizar_lacuna.py
python scripts/calcular_tendencia.py
```

## Resultado atual (top 10 crescimento — AC)

| Curso | Campus | Turno | n | slope |
|---|---|---|---|---|
| Engenharias (FGA) | Gama | Diurno | 6 | 21,73 |
| Eng. Elétrica | Darcy Ribeiro | Diurno | 5 | 20,0 |
| Eng. Mecânica | Darcy Ribeiro | Diurno | 6 | 17,07 |
| Farmácia | Ceilândia | Diurno | 6 | 16,71 |
| Eng. Mecatrônica | Darcy Ribeiro | Diurno | 5 | 15,50 |
| Artes Cênicas | Darcy Ribeiro | Diurno | 6 | 14,89 |
| Gestão de Políticas Públicas | Darcy Ribeiro | Noturno | 5 | 14,24 |
| Pedagogia | Darcy Ribeiro | Noturno | 5 | 12,59 |
| Artes Visuais | Darcy Ribeiro | Diurno | 6 | 12,16 |
| Terapia Ocupacional | Ceilândia | Diurno | 6 | 9,89 |

## Limitações (documentar no artigo)

- O triênio **2022-2024 está incompleto** (~168 registros vs ~440 dos demais). A lacuna
  é **concentrada no campus Darcy Ribeiro** (91% das combinações ausentes), proporcional
  por turno e espalhada por todas as modalidades → sugere recorte institucional pontual
  ou problema de extração, **não** falha aleatória. Tratada no nível da combinação
  (painel desbalanceado), sem imputar valores.
- Como Darcy Ribeiro é o campus mais concorrido (Medicina, Direito etc.) e é o mais
  afetado pelo critério de ≥4 triênios, o **ranking principal subrepresenta os cursos
  de maior interesse público**. Isso deve constar explicitamente na seção de Limitações.
- Cotas específicas (renda+raça+campus+turno+curso) com n=4 são sensíveis a casos
  atípicos; por isso a métrica oficial usa AC, deixando cotas como camada exploratória.

## Requisitos

Python 3.12 (`.venv` do projeto). Bibliotecas: pandas, numpy, openpyxl, matplotlib,
seaborn, jupyter. Veja `requirements.txt`.
