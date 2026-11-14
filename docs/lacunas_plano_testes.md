# Lacunas do plano de testes (Carta, Baralho, Jogador)

**Base:** `PLANO_TESTES.md` × [`requisitos.md`](requisitos.md) × [`cenarios_de_teste.md`](cenarios_de_teste.md) · **Levantamento em:** 2026-11-10

## 1. Resumo

O plano cobre `Carta`, `Baralho` e `Jogador`: cerca de **37 dos 177 cenários unitários**. Ficam de fora **140 unitários e os 23 casos de uso ponta a ponta**.

## 2. Módulos sem nenhum teste

| Módulo | Cenários | Requisitos |
|---|--:|---|
| `jogo.py` (rodada, parda, quem joga primeiro, fuga) | 10 | RF-03, 12, 13, 14, 15 |
| `truco.py` | 18 | RF-20 a 23 |
| `envido.py` | 23 | RF-30, 31, 33, 34, 35 (RF-32 só em parte) |
| `flor.py` | 12 | RF-41, 42, 43 |
| `bot.py` | 14 | RF-50, 51, 55 |
| `cbr.py` | 23 | RF-52, 53 |
| `dados.py` | 15 | RF-54, 56 |
| `interface.py` | 14 | RF-04, RNF-02 |
| `__main__.py` (fluxo e entradas) | 11 | RF-01, 05, 06, RNF-02 |
| Ponta a ponta (`test_e2e.py`) | 23 | critérios de aceite |

Também sem cobertura: RNF-01, 03, 04, 06 e quase todo o RNF-05 (parda, cantos, recusas, fim de partida).

## 3. Lacunas dentro dos três módulos

- **Parda / empate de carta (RF-12, DEF-03):** sem teste de `3C` × `3O`. O CT-CAR-08 ("cenários equivalentes") é vago demais para pegá-lo.
- **Manilhas falsas:** faltam `1` de copas/ouros e `7` de copas/bastos (CAR-04, CAR-05).
- **Envido com figura (DEF-10):** `12E 5E 4O` retorna 5 (esperado 25); flor só de figuras dá 0 (esperado 20). CT-JOG-07/08 não pegam.
- **`mostrar_opcoes` (RF-20, 30, 40):** sem teste, nem o bug da flor que some na 2ª chamada (JGD-07, JGD-08).
- **Entradas inexistentes:** número 8/9 (`KeyError`), naipe "PAUS" (`None`), `classificar_carta` com menos de 3 cartas (`IndexError`).
- **Saída de tela:** `exibir_carta` e `printar_baralho` (precisam de `capsys`).
- **`Baralho`:** `embaralhar` com semente fixa, ausência de repetidas, distribuição 3 + 3 (restam 34), `criar_baralho` duas vezes (duplica para 80).
- **Esconder carta (RF-10):** ausente.

## 4. Erros no próprio plano (conferidos rodando o código)

1. **CT-BAR-02** diz "sem 8, 9 ou 10", mas o baralho **tem** 10, 11 e 12. Contradiz o CT-BAR-03 (10 cartas por naipe). Correto: "sem 8 e 9".
2. **CT-JOG-10** diz que `resetar()` zera os pontos. Ele **mantém `pontos`** (7 continua 7) e não zera `envido` nem `pediu_flor`.
3. **CT-JOG-07** descreve "soma das duas melhores + 20"; o código só soma se as duas cartas valem mais que 0.

4. **CT-CAR-09** espera o rótulo "Média", mas o código devolve `'Media'` sem acento. Com três cartas de mesmo valor (ex.: `3C 3O 3B`) o retorno é `['Media','Media','Baixa']`: nenhuma "Alta", porque o rótulo Baixa sobrescreve o Alta.

Outros pontos: o plano não cita IDs de requisito, não define marcadores, fixtures nem `xfail(strict=True)` para defeitos conhecidos, e os comandos são de PowerShell (o projeto roda em Linux).

## 5. Correção em `cenarios_de_teste.md`

O JGD-06 afirma que `checa_flor` com mão vazia levanta `IndexError`; na verdade retorna `True` (o `all()` sobre lista vazia nem avalia `self.mao[0]`).
