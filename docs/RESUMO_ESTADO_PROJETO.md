# RESUMO DO ESTADO — PROJETO PAS (Programa de Avaliação Seriada) UnB

## Objetivo do projeto
Analisar os dados de notas de corte do PAS da Universidade de Brasília (UnB) por
curso, turno, campus e modalidade de cota, e identificar **cursos com tendência de
crescimento de procura/demanda** ao longo dos triênios. Correlação futura com notas
do ENEM/SISU está prevista, mas **ainda não foi iniciada** (sem dados de ENEM no
projeto até o momento).

## Localização
`/home/gabriel/Projetos/Data Science/PAS`

## Estrutura de dados atual

### 1. Series temporais (triênios) — pasta `diagnosticos/`
Cada triênio tem 3 arquivos:
- `<trienio>.csv` — dados limpos (notas mín/máx por curso/modalidade)
- `<trienio>_auditoria.csv` — versão de auditoria
- `<trienio>_resumo.json` — metadados agregados

Triênios disponíveis: **2018-2020, 2019-2021, 2020-2022, 2021-2023, 2022-2024, 2023-2025**

| Triênio  | Registros | Campi | Cursos | Modalidades | Nota mín (global) | Nota máx (global) |
|----------|-----------|-------|--------|-------------|-------------------|-------------------|
| 2018-2020| 436       | 4     | 88     | 8           | -102.23           | 190.74            |
| 2019-2021| 463       | 4     | 85     | 8           | -98.76            | 192.19            |
| 2020-2022| 449       | 4     | 88     | 8           | -105.49           | 209.07            |
| 2021-2023| 445       | 4     | 86     | 9           | -96.10            | 211.74            |
| 2022-2024| 168       | 3     | 48     | 7           | -105.03           | 173.06            |
| 2023-2025| 345       | 4     | 85     | 9           | -100.43           | 190.33            |

Obs.: o triênio 2022-2024 está **incompleto** (168 registros vs ~440 dos demais) —
provável lacuna de processamento ou dados parciais. Requer verificação.

### 2. Tabelas de corte (formato original Cebraspe) — pasta `tsv/`
Arquivos `YYYY-ZZZZ.tsv` (2018-2020 a 2023-2025). Estrutura de cabeçalho
multi-nível (Curso / Turno / Sistema de Cotas: Escolas Públicas [Renda≤1,5sm,
PPI, PCD+PPI, Não PPI, etc.] / Negros / Universal), com colunas Mín/Máx.
São os dados brutos de notas de corte por cota (escore do PAS, não nota ENEM).

### 3. Planilha recorte — `2022-2024_crop.xlsx`
Sheet `Table 1`, 60 linhas × 22 colunas. Recorte específico do triênio 2022-2024.

### 4. `diagnosticos/resumo_processamento.csv`
Tabela-resumo do processamento por triênio (já incluída acima).

## Esquema das colunas (dados limpos — ex. `2022-2024.csv`)
`Subprograma, Ano, Campus, Curso, Turno, Modalidade, modalidade_normalizada,
escola_publica, faixa_renda, grupo_etnico, pcd, limite_salario_minimo,
Nota Mínima, Nota Máxima`

- Modalidades normalizadas observadas: `AC` (amplas), `CN` (cotas negros),
  `EP_R1_NPPI`, `EP_R1_PPI`, `EP_R2_NPPI`, `EP_R2_NPPI_PCD`, `EP_R2_PPI`
  (escolas públicas, por faixa de renda R1/R2 e grupo étnico PPI/Não-PPI, com/sem PCD)
- Campi: Ceilândia, Darcy Ribeiro (Plano Piloto), Gama (ex.: 2022-2024 → 18/147/3)
- Notas variam de ~-105 a ~+211 (escore do PAS, pode ser negativo)

## Cursos cobertos (exemplos da lista UnB)
Medicina, Psicologia, Direito, Ciência da Computação, Engenharia de Computação,
Odontologia, Medicina Veterinária, Enfermagem, Farmácia, Nutrição, Design,
Relações Internacionais, Agronomia, todas as Engenharias (Civil, Elétrica,
Mecânica, Mecatrônica, Química, etc.), licenciaturas (Matemática, Letras,
História, Pedagogia) — total ~85-88 cursos por triênio completo.

## Estado de processamento / qualidade
- Dados já normalizados (modalidade_normalizada, campi, faixa_renda, grupo_etnico).
- Há arquivos de auditoria pareados por triênio.
- **Lacuna conhecida:** triênio 2022-2024 com volume muito menor (168 vs ~440).

## Próximos passos sugeridos (para a outra LLM detalhar)
1. Consolidar os 6 triênios numa série temporal única por
   (Curso, Campus, Turno, Modalidade) — CSV `cursos_serie_2018_2024.csv`.
2. Tratar a inconsistência do triênio 2022-2024 (investigar perda de registros).
3. Calcular tendência de crescimento (regressão/slope ou variação % entre
   triênios) da nota de corte por curso → "cursos em alta".
4. (Futuro, não iniciado) Integrar notas de corte SISU/ENEM por curso para
   correlação — **bloqueado**: não há dados de ENEM no projeto; fontes públicas
   de série histórica 2018-2024 do SISU são fragmentadas/inexistentes (portais
   mostram só ano corrente); microdados INEP exigiriam download pesado (~50GB).

## Observação importante para a outra LLM
- As "notas" aqui são **escore do PAS** (próprio do processo seriado da UnB),
  NÃO nota do ENEM. Qualquer correlação com ENEM exige uma fonte externa ainda
  não obtida.
- O ambiente Python do projeto é `.venv` (python3.12, pandas instalado).
