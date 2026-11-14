# Status dos Testes — Truco Gaudério com CBR

**Levantamento em:** 2026-11-07 · **Base:** `main` @ `ef08721` · **Fonte dos cenários:** [`cenarios_de_teste.md`](cenarios_de_teste.md) v1.0

## 1. Resumo

| Item | Situação |
|---|---|
| Cenários **especificados** (documento) | **200** — 177 unitários (§4) + 23 de caso de uso ponta a ponta (§5) |
| Testes **implementados** (código) | **0** — não existe `tests/`, `conftest.py`, `pytest.ini` nem fixtures no repositório |
| Testes **executados** | **0** |
| Ambiente de execução | `pytest` **não instalado**; `pandas`/`scikit-learn` não instalados no Python do sistema; sem `.venv`; `requirements.txt` lista só `pandas` e `scikit-learn` |
| Meta de aceite (§7 dos cenários) | ≥ 150 cenários executáveis → **0 / 150** |

Em resumo: o projeto está na fase de **especificação**. Os cenários e o catálogo de defeitos esperados existem; falta implementar a suíte.

## 2. Testes unitários — por módulo

Todos com status **não implementado**. A coluna "Defeitos esperados" indica quantos cenários estão previstos como `xfail(strict=True)` por divergência do código em relação ao requisito.

| Módulo | Arquivo-alvo | Seção | Cenários | Implementados | Com defeito previsto (`✘`) |
|---|---|---|--:|--:|---|
| Baralho | `test_baralho.py` | 4.1 | 10 (BAR-01…10) | 0 | — |
| Carta / pontos | `test_carta.py` | 4.2 | 16 (CAR-01…16) | 0 | CAR-06 (DEF-03) |
| Regras de rodada | `test_jogo.py` | 4.3 | 10 (JOG-01…10) | 0 | JOG-02, 07, 10 |
| Jogador humano | `test_jogador.py` | 4.4 | 11 (JGD-01…11) | 0 | JGD-05 (parcial, DEF-10), 08, 10 |
| Truco | `test_truco.py` | 4.5 | 18 (TRU-01…18) | 0 | TRU-02, 09, 12 (parc.), 13 (parc.), 17 (1 linha), 18 |
| Envido | `test_envido.py` | 4.6 | 23 (ENV-01…23) | 0 | ENV-04, 07, 08, 10, 11, 12, 15, 16 (parc.), 20, 21, 23 |
| Flor | `test_flor.py` | 4.7 | 12 (FLO-01…12) | 0 | FLO-03…07, 10 (parc.), 12 |
| Bot | `test_bot.py` | 4.8 | 14 (BOT-01…14) | 0 | BOT-05 (linhas 3, 11), 08, 09, 11 |
| IA — CBR | `test_cbr.py` | 4.10 | 23 (CBR-01…22 + 01b) | 0 | CBR-01b, 06 (parc.), 07, 08, 10, 11 (parc.), 13, 15, 21, 22 |
| Registro de casos | `test_dados.py` | 4.11 | 15 (DAD-01…15) | 0 | DAD-03…07, 09 |
| Interface | `test_interface.py` | 4.12 | 14 (INT-01…14) | 0 | INT-07, 09, 11, 12 (parc.) |
| Fluxo principal / entradas | `test_main_entradas.py` | 4.13 | 11 (MAIN-01…11) | 0 | MAIN-01…06 (parc.), 08 |
| **Total unitário** | | | **177** | **0** | |

## 3. Testes de caso / cenário de uso (ponta a ponta)

Arquivo-alvo: `test_e2e.py` · Seção 5 dos cenários · **23 casos (UC-01…UC-23) — 0 implementados.**

| Grupo | Casos | Previsão com o código atual |
|---|---|---|
| Fluxo de mão e pontuação | UC-02, 03, 04, 09, 10, 12, 13, 15, 20 | ✔ devem passar (9) |
| Fim de partida / alternância do mão | UC-01, 18 | ✘ DEF-02 (12 em vez de 30), DEF-21 |
| Parda / empates de carta | UC-05, 06, 07, 08 | ✘ DEF-03 |
| Truco com valor | UC-11 | ✘ DEF-04 |
| Envido | UC-14, 16 | ✘ DEF-07, DEF-09 |
| Flor | UC-19, 21, 22 | ✘ DEF-14, DEF-12, DEF-11 |
| Entradas inválidas | UC-17 | ✘ DEF-24, DEF-13 |
| Partida com `Cbr` real | UC-23 | ✘ depende da semente (DEF-19/17) |

Previsão: **9 passam, 14 `xfail`** (status "(p)" = previsto por leitura do código, a confirmar ao rodar).

## 4. O que já existe de apoio

- **Catálogo de defeitos** DEF-01…DEF-25 em `cenarios_de_teste.md` §3, vários já confirmados por sondagem executada, marcados `(c)`.
- **Estratégia, fixtures e marcadores** definidos (§1): `cwd_tmp`, `cbr_real`, `cbr_sintetico`, `cbr_stub`, `fake_jogador`, `entradas`, `baralho_armado`, `rodar_main`; marcadores `req, exc, msg, loop, ifs, call, input_, ret, ia, e2e`.
- **Rastreabilidade** requisito → cenário (§6) e roteiro do vídeo (§7).

## 5. Pendências e bloqueios

1. **Ambiente:** criar `.venv`, instalar `pytest`, `pytest-cov`, `pandas`, `scikit-learn`; acrescentar `pytest`/`pytest-cov` ao `requirements.txt` (ou a um arquivo de dev).
2. **`tests/fixtures/base_original.csv`:** a base está ausente; o documento a descreve como a separada por vírgula do commit `3b63d88`. **Divergência a validar:** o `dbtrucoimitacao_maos.csv` atual da `main` tem cabeçalho com TAB (27.515 linhas de dados), enquanto `cbr.py`/`dados.py` leem com vírgula (`read_csv` sem `sep`). Isso é o DEF-01 e ainda se aplica.
3. **Scaffolding:** `tests/conftest.py`, registro dos marcadores (`pytest.ini`) e as fixtures acima.
4. **Confirmar os status `(p)`** rodando a suíte; só `(c)` foi verificado por execução.
5. **Ordem sugerida** (do documento): conftest → Carta/Baralho/Jogo/Jogador → Truco/Envido/Flor → Bot + CBR → Dados/Interface → `__main__`/E2E → cobertura de ramos.

## 6. Próximo passo sugerido

Montar o ambiente e o `conftest.py`, e implementar primeiro os módulos rápidos e determinísticos (Baralho, Carta, Jogo, Jogador: 47 cenários), que já geram resultados e validam a estratégia de `xfail strict`.
