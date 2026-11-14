# Plano de Testes — Mateus (Truco Gaudério com CBR)

**Base:** [`requisitos.md`](requisitos.md) · [`cenarios_de_teste.md`](cenarios_de_teste.md) · [`lacunas_plano_testes.md`](lacunas_plano_testes.md) · **Data:** 2026-11-13

**Índice:** §1 Divisão do trabalho · §2 Estratégia · §3 Andamento · §4 Regras (jogo, truco, envido, flor) · §5 Interface, fluxo principal e E2E (inclui RNFs sem dono) · §6 Lacunas nos módulos da Amanda · §7 Tabela de defeitos · §8 Observações das lacunas e defeitos.

Referências cruzadas: **Obs. regras n** (lista no fim do §4), **Obs. interface n** (fim do §5) e **Obs. lacunas n** (§8).

## 1. Divisão do trabalho

| Responsável | Escopo |
|---|---|
| Amanda | `PLANO_TESTES.md`: Carta, Baralho e Jogador |
| Gabriel | IA: `bot.py`, `cbr.py` e `dados.py` (UC-23, partida com `Cbr` real) |
| **Mateus** | Tudo o que o plano da Amanda não aborda: `jogo.py`, `truco.py`, `envido.py`, `flor.py`, `interface.py`, `__main__.py`, ponta a ponta (UC-01 a UC-22), lacunas nos módulos da Amanda e RNFs sem dono |

Para não sobrepor, os testes ficam em arquivos próprios (`test_jogo.py`, `test_truco.py`, `test_envido.py`, `test_flor.py`, `test_interface.py`, `test_main_entradas.py`, `test_e2e.py`, `test_lacunas.py`). O `conftest.py` é compartilhado: só se acrescenta, sem alterar o que já existe.

## 2. Estratégia

- **Oráculo = requisitos.** Quando o código diverge, o teste é escrito contra o requisito e marcado `@pytest.mark.xfail(strict=True, reason="DEF-nn")`.
- **Sem alterar o código-fonte**; `input()` e `print()` via `monkeypatch` e `capsys`.
- **IA isolada:** nos meus testes o CBR é sempre um stub, para não depender do trabalho do Gabriel.
- **Marcadores:** `req`, `exc`, `msg`, `loop`, `ifs`, `call`, `input_`, `ret`, `ia`, `e2e` (registrados no `pytest.ini`).
- **Legenda de status:** `✔` deve passar · `✘ DEF-nn` deve falhar (defeito) · `(c)` confirmado por execução · `(p)` previsto por leitura do código.
- **Execução** (da raiz do repositório):

```bash
.venv/bin/python -m pytest -v -rxX --tb=short
.venv/bin/python -m pytest --cov=truco --cov-branch --cov-report=term-missing
```

## 3. Andamento

**Escopo enxuto:** a implementação cobre só os cenários principais de cada arquivo (para permitir explicar as funções e o funcionamento). Os demais cenários das tabelas das seções 4 a 6 continuam especificados, mas **não implementados**.

| Arquivo | Cenários implementados | Situação |
|---|---|---|
| `test_jogo.py` | 10 (26 casos) | Implementado: 21 passam, 5 `xfail` |
| `test_truco.py` | 7: TRU-01, 02, 03, 04, 06, 09, 17 | Implementado: 14 passam, 3 `xfail` (DEF-04, DEF-05, DEF-34 proposto) |
| `test_envido.py` | 10: ENV-01 a 07, 11, 13 | Implementado: 7 passam, 3 `xfail` (DEF-07, 08, 09) |
| `test_flor.py` | 6: FLO-01 a 05, 08 | Implementado: 3 passam, 3 `xfail` (DEF-23, 12, 11) |
| `test_e2e.py` | 7: UC-02, 03, 05, 09, 10, 11, 13 | Implementado: 5 passam, 2 `xfail` (DEF-03, DEF-04) |
| `test_interface.py`, `test_main_entradas.py`, `test_lacunas.py` | — | Fora do escopo enxuto (não implementados) |

**Total da suíte atual** (`.venv/bin/python -m pytest`): 49 passam e 16 `xfail` strict, nenhuma falha.

**Ordem seguida:** `jogo` → `truco`/`envido`/`flor` → `e2e`. O E2E usa `rodar_main` (em `test_e2e.py`): baralho armado, CBR e Dados falsos e roteiro de entradas; `EOFError` encerra a execução.

---

# Cenários

## 4. Regras do jogo: jogo, truco, envido e flor

Tipo de documento: referência (status dos cenários de teste por módulo de regras). Fonte dos cenários: `cenarios_de_teste.md` §4.3, §4.5, §4.6 e §4.7. Legenda: `✔` o código atual passa; `✘ DEF-nn` o código atual falha (defeito do catálogo §3); `(c)` confirmado por execução; `(p)` previsto por leitura do código, ainda a confirmar ao rodar a suíte.

### Regras de rodada (`jogo.py`)

Arquivo-alvo: `tests/test_jogo.py` (implementado). Resultado real da execução com `.venv/bin/python -m pytest tests/test_jogo.py`: **26 testes coletados, 21 passam e 5 xfail** (`xfail strict`), nenhum falha.

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| JOG-01 | `verificar_carta_vencedora` com pares manilha×manilha, manilha×comum e comum×comum, nas duas ordens | Devolve a carta maior | req, call, ret | RF-11 | ✔ (c) 8 casos passam (o teste usa 8 pares, não 6) |
| JOG-02 | Empate de cartas (3C × 3O; 7C × 7B; 12E × 12O) | Resultado “parda” | req, ret | RF-12 | ✘ DEF-03 (c) 3 xfail |
| JOG-03 | `verificar_ganhador` | Devolve a vencedora e imprime `Carta ganhadora: …` | ret, msg | RF-04 | ✔ (c) |
| JOG-04 | `adicionar_rodada` com ganhador = carta1 / carta2 / objeto estranho | Retorna `1` e `j1.rodadas+1` / `2` e `j2.rodadas+1` / `"Erro"` sem alterar | ifs, ret | RF-14 | ✔ (c) |
| JOG-05 | `quem_joga_primeiro` (ganhou carta1 / carta2) | Flags `primeiro` coerentes | ifs | RF-13 | ✔ (c) |
| JOG-06 | `quem_inicia_rodada`: 4 combinações de (`rodadas == 0` em ambos?) × (`j1.ultimo` / `j2.ultimo`) | Alterna quem é “primeiro” só quando ambos têm 0 rodadas | ifs | RF-03 | ✔ (c) 4 casos passam |
| JOG-07 | `jogador_fugiu(...)` | Imprime `Jogador fugiu!`; “mão” da próxima = quem **não** fugiu | msg, req | RF-15 | Parcial (c): fuga do jogador 2 ✔ (a mensagem sai e j1 fica como mão); fuga do jogador 1 ✘ xfail, defeito **DEF-33 (proposto)** (a função sempre define j1 como primeiro; código morto, ver Obs. regras 8) |
| JOG-08 | `criar_jogador` / `criar_bot` com baralho cheio e com 2 cartas | Objeto com nome e 3 cartas (baralho fica com 37) / `IndexError` | call, exc | RF-02 | ✔ (c) 4 casos passam |
| JOG-09 | Estado inicial de `Jogo()` | `rodadas == []`, `trucoPontos == 1` | ret | — | ✔ (c) |
| JOG-10 | O “mão” alterna entre mãos consecutivas | “Mão” da mão 2 ≠ “mão” da mão 1 (partida real) | req | RF-03 | ✘ DEF-21 (c) xfail |

### Truco (`truco.py`)

Arquivo-alvo: `tests/test_truco.py` (a criar). Notação: o humano é o jogador 1 (`quem_pediu=1`) e o bot responde via `avaliar_truco` (0 = recusar, 1 = aceitar, 2 = aumentar).

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| TRU-01 | `Truco()` | `valor_aposta=1`, `estado_atual=""`, `jogador_bloqueado=0` | ret | RF-23 | ✔ (c) |
| TRU-02 | Humano canta Truco; bot aceita | Retorna `True`; `estado="truco"`; **valor da mão = 2** | req, ret | RF-20/23 | ✘ DEF-04 (c) valor fica 1 |
| TRU-03 | Humano canta; bot recusa | Retorna `False`; humano +1; mão encerra | req, ret | RF-22 | ✔ (c) |
| TRU-04 | Truco → bot aumenta → humano aceita Retruco (`'1'`) | `True`; valor 3; `estado="retruco"` | req | RF-20/23 | ✔ (c) |
| TRU-05 | Retruco → humano recusa (`'0'`) | `False`; **bot** +2 | req | RF-22 | ✔ (c) |
| TRU-06 | Retruco → humano aumenta (`'2'`) → bot aceita Vale 4 | `True`; valor 4; `pediu_truco=True` em ambos | req | RF-20 | ✔ (c) |
| TRU-07 | Vale 4 recusado pelo bot | Humano +3; `False` | req | RF-22 | ✔ (c) |
| TRU-08 | Vale 4 com humano digitando `'2'` (aumentar) e depois `'1'` | `'2'` rejeitado, pergunta de novo; `'1'` aceita (início/fim do laço) | loop, input_ | RF-21 | ✔ (c) (chamando `pedir_vale_quatro(..., 2, ...)` direto) |
| TRU-09 | Após Vale 4 aceito, novo canto de qualquer jogador | Retorna `None`; valor permanece 4 | req, ifs | RF-21 | ✘ DEF-05 (c) valor cai para 3; só aparece no fluxo real, porque `pedir_vale_quatro` não grava o estado `vale_quatro` |
| TRU-10 | Mesmo jogador canta 2 vezes seguidas | 2ª chamada retorna `None` | ifs, ret | RF-21 | ✔ (c) |
| TRU-11 | Bot canta (`quem_pediu=2`); humano responde `'0'`, `'1'`, `'2'` | `False` e bot +1 / `True` / escala para Retruco | input_, ret | RF-22 | ✔ (c) |
| TRU-12 | Entradas do humano: `'9'`, `'-1'`, `'5'`, depois `'1'`; e `'abc'`, `''`, `'1.5'` | Inválidos numéricos repetem a pergunta e aceitam `'1'`; não numéricos devem dar mensagem amigável | loop, input_, exc, msg | RF-22, RNF-02 | ✔ laço (c); ✘ DEF-24 (c) `ValueError` |
| TRU-13 | `retornar_valor_aposta()` após cada etapa; `retornar_quem_fugiu()` | 1, 2, 3, 4; valor inteiro (jogador) | ret | RF-23 | ✘ DEF-04 (c) `valor_aposta` fica 1 (valor); ✘ DEF-06 (c) (`retornar_quem_fugiu`) |
| TRU-14 | `resetar()` após Vale 4 | Volta ao estado inicial (TRU-01) | req | RF-02 | ✔ (c) |
| TRU-15 | `inverter_jogador_bloqueado` com bloqueado = 0, 1, 2 | 1, 2, 1 | ifs, ret | RF-21 | ✔ (c) |
| TRU-16 | `inicializar_jogador_bloqueado(x)` | `jogador_bloqueado == x` | call | RF-21 | ✔ (c) |
| TRU-17 | Tabela de decisão de `controlador_truco`: estado ∈ {`""`, `truco`, `retruco`, `vale_quatro`, `outro`} × (`quem_pediu == bloqueado`: sim/não) = 10 combinações | `None` se `vale_quatro` ou bloqueado; senão canto do próximo nível; `outro` ⇒ `None` | ifs, call | RF-20/21 | ✔ 9 (c, inclui `vale_quatro`); ✘ (c) na linha `retruco` com `quem_pediu` ≠ bloqueado (chama `pedir_retruco` de novo, não o Vale 4; candidato DEF-34 proposto); DEF-05 só no fluxo real (ver Obs. regras 1) |
| TRU-18 | Propriedade: a aposta nunca diminui em qualquer sequência de cantos | `valor_n+1 ≥ valor_n` | req | RF-23 | ✘ DEF-05 (c) |

### Envido (`envido.py`)

Arquivo-alvo: `tests/test_envido.py` (a criar). Parâmetros comuns: pontos de envido humano/bot, `placar` e “mão”. Para o bot, `avaliar_envido` é roteirizado (0 = recusar, 1 = aceitar, 2 = Real, 3 = Falta).

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| ENV-01 | `Envido()` | `valor_envido=2`, `estado_atual=0` | ret | RF-31 | ✔ (c) |
| ENV-02 | Humano canta Envido (6), bot aceita; 30 × 20 | Humano +2; vencedor 1; caixa “Venceu o envido com 30 pontos” | req, msg | RF-31/32 | ✔ (c) |
| ENV-03 | Idem com 20 × 28 | Bot +2; vencedor 2 | req | RF-32 | ✔ (c) |
| ENV-04 | Empate 25 × 25, com “mão” = humano e depois “mão” = bot | Vence o “mão” | req, call | RF-32 | ✘ DEF-07 (c) humano sempre |
| ENV-05 | Bot recusa Envido | Humano +1; `quem_fugiu=2`; **sem** caixa de vencedor | ifs, ret | RF-33 | ✔ (c) |
| ENV-06 | Bot canta (`quem_pediu=2`), humano recusa (`'0'`) | Bot +1 | input_ | RF-33 | ✔ (c) |
| ENV-07 | Real Envido direto (7), aceito | Valor **3** | req | RF-31 | ✘ DEF-08 (c) vale 5 |
| ENV-08 | Real Envido direto, recusado | Cantor +1 | req | RF-33 | ✘ DEF-08 (c) +2 |
| ENV-09 | Envido → bot responde Real (2) → humano aceita | Valor acumulado **5** | req | RF-31 | ✔ (c) (ver Obs. regras 4) |
| ENV-10 | Envido → Real → Falta (encadeamento completo) | Valor = falta do líder; vencedor correto | req | RF-31/34 | ✘ DEF-09 (c) com 5×3 dá 9 (= 12 − 3); esperado 30 − 5 |
| ENV-11 | Falta Envido direto com placar humano 5 × bot 3, aceito | Valor = **30 − 5 = 25** | req, call | RF-34 | ✘ DEF-09 (c) vale 9 |
| ENV-12 | Falta Envido recusado | Cantor ganha acumulado + 1 | req | RF-33 | ✘ DEF-09 (c) +5 |
| ENV-13 | 2º canto na mesma mão (estado ≠ 0) | `None`, sem efeito | ifs, ret | RF-30 | ✔ (c) |
| ENV-14 | `quem_pediu == jogador_bloqueado` com `estado=0` | `None` | ifs | RF-30 | ✔ (c) |
| ENV-15 | `tipo` inválido (0, 5, 9, −1) | Rejeitado: nenhum ponto e nenhuma caixa de “vencedor” | call, msg | RF-30 | ✘ DEF-23 (c) só para tipo 5, 9 e −1 (imprime caixa com vencedor 0); tipo 0 devolve `None` e passa, testar sem `xfail` (ver Obs. regras 3) |
| ENV-16 | Humano responde Envido com `'4'`, `'-1'`, `'2'`; e com `'abc'` | `'4'`/`'-1'` repetem; `'2'` ⇒ Real; `'abc'` ⇒ erro tratado | loop, input_, exc | RF-31 | ✔ laço (p); ✘ DEF-24 (c) |
| ENV-17 | Pergunta de Real Envido: opções {0,1,2}; `'3'` | `'3'` rejeitado | loop, input_ | RF-31 | ✔ (c) |
| ENV-18 | Pergunta de Falta Envido: opções {0,1}; `'2'` | `'2'` rejeitado | loop, input_ | RF-31 | ✔ (c) |
| ENV-19 | `definir_pontos_jogadores` | Copia `envido` de cada jogador | call | RF-32 | ✔ (c) |
| ENV-20 | `resetar()` | Todos os campos iniciais, incluindo `jogador2_pontos` | req | RF-02 | ✔ (c) `resetar()` zera os pontos do jogador 2 (ver Obs. regras 2) |
| ENV-21 | Captura de saída em qualquer canto | Sem linhas de depuração (`1`, `2`, `3`, `4`) | msg | RNF-02 | ✘ DEF-18 (c) |
| ENV-22 | Tabela de decisão de `controlador_envido`: (estado = 0 / ≠ 0) × (tipo = igual ao estado?) × (bloqueado = quem_pediu?) × tipo ∈ {6, 7, 8, outro} | Só executa quando estado = 0, não bloqueado e tipo válido | ifs, call | RF-30 | ✔ exceto `outro` (DEF-23) |
| ENV-23 | Pontuação não ultrapassa o placar final (jogador com placar−1 ganha Falta) | `pontos == limite` | req | RF-06 | ✘ DEF-25 (c) no módulo (29 pts → 31, sem teto). O jogo real encerra em 12 (DEF-02), então “30” só vale ao corrigir DEF-02 |

### Flor (`flor.py`)

Arquivo-alvo: `tests/test_flor.py` (a criar).

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| FLO-01 | Só o bot tem flor | Bot +3; vencedor 2; caixa | req, msg | RF-41 | ✔ (c) |
| FLO-02 | Só o humano tem flor | Humano +3; vencedor 1 | req | RF-41 | ✔ (c) |
| FLO-03 | Ninguém tem flor, `pedir_flor` chamado | Nenhum ponto; **sem** caixa de vencedor | req, msg | RF-40 | ✘ DEF-23 (c) imprime “Jogador 2 venceu a flor” |
| FLO-04 | Ambos com flor, Contra-flor aceita; pontos de flor 38 × 35 | Vencedor 38; **+6** | req | RF-42 | ✘ DEF-12 (c) compara pontos de envido |
| FLO-05 | Ambos com flor, recusa da Contra-flor | Cantor +3 | req | RF-42 | ✘ DEF-11 (c) +4 |
| FLO-06 | Contra-flor e o resto aceita | Valor = resto + 6 | req | RF-42 | ✘ DEF-12 (c) valor 3 |
| FLO-07 | Empate de flor | Vence o “mão” | req | RF-43 | ✘ (c) com 33×33 sempre +6 ao humano (sem parâmetro de mão); **sem DEF numerado** |
| FLO-08 | 2º `pedir_flor` na mesma mão | Ignorado (nenhum ponto novo) | ifs | RF-41 | ✔ (c) |
| FLO-09 | `resetar_flor()` | `valor_flor=3`, `estado=""`, vencedor 0 | req | RF-02 | ✔ (c) |
| FLO-10 | `decisao_jogador` com entradas `'2'`, `'-1'`, `'1'` / `'x'` | Repete até 0/1; `'x'` ⇒ erro tratado | loop, input_, exc | RF-42 | ✔ laço (p); ✘ DEF-24 (c) |
| FLO-11 | Fronteira `bot.pontos < int(humano.pontos/1.5)` → Resto vs. Contra-flor: (h,b) = (0,0)→CF; (1,0)→CF; (2,0)→Resto; (3,1)→Resto; (3,2)→CF; (12,7)→Resto; (12,8)→CF | Estado indicado | ifs, call | RF-42 | ✔ (c) todos os 7 pares |
| FLO-12 | Decisão entre Contra-flor e “resto” é do jogador | O humano escolhe | req | RF-42 | ✘ (c) estado definido só pelo placar; `decisao_jogador` sempre pergunta “Jogador 1”, mesmo quando ele cantou; **sem DEF numerado** |

### Observações das regras (Obs. regras n)

Conferência dos cenários contra `truco/*.py` (nada foi alterado no repositório). Itens marcados “a confirmar” não foram executados.

1. **TRU-17, linha `retruco`.** `controlador_truco` chama `pedir_retruco` também no estado `retruco` (`truco/truco.py:42-43`), não `pedir_vale_quatro`: a linha com `quem_pediu` ≠ bloqueado falha (c). A linha `vale_quatro` passa (c), e a contagem “9 ✔” está correta. O DEF-05 só aparece no fluxo real (TRU-09/18), porque `pedir_vale_quatro` não grava o estado `vale_quatro`. Já está registrado em `requisitos.md` §8, mas não tem DEF numerado (sugestão: DEF-34, proposto). Além disso, quando o estado é `outro`, `inicializar_jogador_bloqueado` já foi chamado antes do `return None` (efeito colateral, `truco.py:31-46`).
2. **ENV-20.** `Envido.resetar()` zera `jogador1_pontos` e `jogador2_pontos` (`truco/envido.py:216-217`). Confirmado por execução (c): o cenário passa e o status “✘ (p)” do original estava errado. ENV-20 deixa de ser candidato a DEF.
3. **ENV-15 (tipo 0).** Com `tipo = 0` e `estado_atual = 0`, o primeiro `if` de `controlador_envido` (`tipo == self.estado_atual`) devolve `None` antes de qualquer caixa (`envido.py:32-33`). Confirmado (c): só `tipo` 5, 9 e −1 imprimem a caixa com vencedor 0 (DEF-23). O tipo 0 deve ser testado sem `xfail`.
4. **ENV-07 e ENV-09.** O valor 5 de ENV-09 coincide com o valor 5 que `real_envido` fixa sempre (`envido.py:102`); passa por acaso, não porque o encadeamento acumula (Envido 2 + Real 3). O requisito também prevê Envido + Envido = 4, que o código não implementa (não há resposta “Envido” sobre Envido). Sem cenário nem DEF para isso.
5. **FLO-05.** A recusa de Contra-flor ou de “resto” só faz `jogador2.pontos += 4` (`truco/flor.py:28-40`); `contraflor(2, …)` é o ramo de aceitação (`flor.py` ~419-431) e ignora o parâmetro `quem_pediu`. Se o humano cantar a flor, o ponto vai para o bot. Além disso, `decisao_jogador` pergunta sempre ao “Jogador 1”, mesmo quando ele cantou (FLO-12). Após uma recusa `quem_venceu_flor` permanece 0 e `mostrar_vencedor_flor` ainda imprime a caixa “Jogador 2 venceu a flor” (`interface.py:61-67`; mesma raiz do DEF-23). Nem o parâmetro ignorado nem a caixa após recusa estão no catálogo.
6. **FLO-06.** `contraflor_resto` atribui `self.valor_envido` (atributo inexistente em `Flor`; `flor.py:77-81`), então o valor da flor nunca muda, e os dois ramos do `if` são idênticos. É a mesma causa do DEF-12, mas o detalhe do atributo errado não consta lá.
7. **TRU-14.** `Truco.resetar()` cria `jogador_aumentou2` / `jogador_aumentou4` (`truco.py:172-173`), que não existem em `__init__`, e não zera `jogador_retruco` / `jogador_vale_quatro`. O cenário só verifica valor, estado e bloqueado, então não detecta isso.
8. **JOG-01, JOG-07, JOG-10 (suíte já implementada).** (a) JOG-01 usa 8 pares, não 6 como no original. (b) JOG-07 foi dividido em dois testes; o do jogador 1 está `xfail` com `reason="DEF: …"` sem número. Sugiro registrar DEF-33 (proposto: “`jogador_fugiu` sempre define o jogador 1 como mão”, RF-15). Além disso, `jogador_fugiu` não é chamada pelo `__main__`: as chamadas estão comentadas (`truco/__main__.py:200` e `204`; a de 204 também tem assinatura incompleta), portanto a função é código morto. (c) JOG-10 é um teste estático (procura `quem_inicia_rodada` no texto de `__main__.py`), não uma partida real como diz o cenário. Isso comprova a ausência da chamada, mas não o comportamento.
9. **JOG-06.** O teste passa nos 4 casos, mas `quem_inicia_rodada` é assimétrica: no ramo `j1.ultimo` ela marca `j2.ultimo = True`, no ramo `j2.ultimo` ela não marca `j1.ultimo` (`jogo.py:75-85`), então a alternância não se sustenta em chamadas repetidas. O `__main__` também só inicializa `jogador2.ultimo = True` (`__main__.py:172`). Hipótese a confirmar; não coberta por cenário.
10. **Mensagens.** Em `pedir_retruco`, a resposta `2` imprime “pediu Retruco” mesmo quando o próximo é Vale 4 (`truco.py:119`), já citado em `requisitos.md` §8. A pergunta de `pedir_truco` não traz o prefixo “Jogador” (`truco.py:63`). Ambos são relevantes só para cenários `msg`, que não existem para esses textos.

## 5. Interface, fluxo principal e ponta a ponta

Documento de **referência** (Diátaxis): lista os cenários de `docs/cenarios_de_teste.md` §4.12, §4.13 e §5 com os IDs originais. Status: `✔` deve passar com o código atual; `✘ DEF-nn` deve falhar (defeito catalogado, marcado `xfail(strict=True)`); `(c)` confirmado por sondagem; `(p)` previsto por leitura. Oráculo: `docs/requisitos.md`.

### Interface (`tests/test_interface.py`)

Captura de saída com `capsys` sobre `truco/interface.py`.

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| INT-01 | `mostrar_carta_jogada('Ana', 3 de OUROS)` | `Ana jogou a carta: 3 de OUROS` | `msg` | RF-04 | ✔ (c) |
| INT-02 | `mostrar_carta_ganhadora` e `mostrar_ganhador_rodada` | Textos esperados | `msg` | RF-04 | ✔ (p) |
| INT-03 | `mostrar_ganhador_jogo('Ana')` | `Ana ganhou o jogo` | `msg` | RF-05 | ✔ (c) |
| INT-04 | `mostrar_placar_total` | Caixa com título "Pontuação Total" e 2 linhas "N Pontos Acumulados" | `msg` | RF-04 | ✔ (c) |
| INT-05 | `mostrar_placar_rodadas` | Caixa "Rodadas da Partida Atual" | `msg` | RF-04 | ✔ (p) |
| INT-06 | `mostrar_vencedor_flor` com vencedor 1 e com vencedor 2 | Cada jogador aparece na linha certa | `msg` | RF-41 | ✔ (c para 1) |
| INT-07 | `mostrar_vencedor_flor(0, ...)` | Não apresenta vencedor | `msg` | RF-41 | ✘ DEF-23 (c) |
| INT-08 | `mostrar_vencedor_envido` com vencedor 1 e com vencedor 2 | Vencedor e perdedor corretos, com pontos | `msg` | RF-32 | ✔ (c para 2) |
| INT-09 | `mostrar_vencedor_envido(0, ...)` (empate/sem vencedor) | Mensagem neutra | `msg` | RF-32 | ✘ DEF-23 (c) |
| INT-10 | `mostrar_placar_total_jogador_fugiu(j, ...)` | `Jogador <nome> fugiu!` | `msg` | RF-15 | ✔ (p) |
| INT-11 | `mostrar_jogador_opcoes(nome)` | Informa **quem** é o "mão" | `msg` | RF-03 | ✘ (p) texto fixo "Jogador 1 é mão" |
| INT-12 | `border_msg` com 1 linha, 3 linhas, linha vazia, `indent` 0/1/3, `width` menor que a linha, `title` | Caixa alinhada (linhas de mesmo comprimento) | `call`, `ret` | RNF-02 | ✔ (p), exceto `width` menor que a linha, que (p) quebra o alinhamento |
| INT-13 | `desenhar_cartas('3 de OUROS')` por naipe; `exibir_cartas([])`; `exibir_cartas(["3 de OUROS", ...])` (recebe strings, não `Carta`) | Símbolo ♦/♣/♥/♠ correto; lista vazia sem erro; 9 linhas por carta, lado a lado | `call`, `msg` | RF-04 | ✔ (p) |
| INT-14 | `limpar_tela` com `os.system` substituído | Chama `clear` | `call` | RNF-02 | ✔ (p) |
| INT-15 | `exibir_unica_carta` com uma carta | Desenho da carta com linhas na ordem correta | `call`, `msg` | RF-04 | ✘ (a confirmar) saída transposta; função não é chamada em `truco/` (código morto); sem DEF |
| INT-16 | `mostrar_pediu_truco(nome)` | Imprime `<nome> pediu truco e o pedido já foi aceito, escolha outra jogada!` (texto conferido em `interface.py:84`) | `msg` | RF-20 | ✔ (p) |

### Fluxo principal e entradas do usuário (`tests/test_main_entradas.py`)

Executado via `rodar_main` (nomes + roteiro de entradas, *seed* fixa, CBR *stub*) sobre `truco/__main__.py`. Menu do humano com 3 cartas: `0`-`2` jogam carta, `4` Truco, `5` Flor, `6`/`7`/`8` Envido/Real Envido/Falta Envido, `9` ir ao baralho.

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| MAIN-01 | Nomes `''`, `'Ana'`, `'José'`, `'A'*200`, com emoji | Aceita; caixas de placar não quebram; `''` gera nome padrão ou é recusado | `input_` | RNF-02 | ✘ (p) `''` é aceito e exibido vazio |
| MAIN-02 | Tabela de entradas do menu com 3 cartas: `0`, `1`, `2`, `3`, `4`, `5` (sem flor), `6`, `9`, `10`, `-1`, `' 1 '`, `''`, `'abc'`, `'0.5'`, `'1,3'` | `0`-`2` jogam; `4` e `6`-`9` são ações; `5` sem flor, `10` e `-1` dão "Selecione um valor válido!"; `3` é inválido; não numéricos dão mensagem sem encerrar | `input_`, `msg`, `ifs`, `loop` | RF-10, RNF-02 | `0`,`1`,`2`,`4`,`6`-`9`,`' 1 '` ✔ (p) · `3` ✘ DEF-13 (c) · `''`,`'abc'`,`'0.5'`,`'1,3'` ✘ DEF-24 (c) (`ValueError`) |
| MAIN-03 | Menu com 2 cartas (2ª rodada): `0`, `1`, `2`, `4`, `5`, `6`, `7`, `8`, `9` | `0`,`1` jogam; `4` e `9` são ações; `2` inválido; `5`-`8` indisponíveis (só na 1ª rodada) e dão "Selecione um valor válido!" | `input_`, `ifs` | RF-30 | `2` ✘ DEF-13 (p) · `6`-`8` ✔ (p) |
| MAIN-04 | Menu com 1 carta (3ª rodada): `0`, `1`, `4`, `9` | `0` joga; `1` inválido; Truco indisponível (o menu só o mostra com 2 ou mais cartas) | `input_`, `ifs` | RF-20 | `1` com 1 carta ✘ DEF-13 (c) (`IndexError` em `pop(1)`); o laço aceita `4` mesmo sem aparecer no menu ✘ (p), sem DEF |
| MAIN-05 | Fim da partida: entrada `0` sempre, 5 sementes | A partida termina; vencedor com 30 ou mais e perdedor com menos de 30; mensagem "ganhou o jogo" | `loop`, `req` | RF-01/05 | ✘ DEF-02 (c) termina em 12 |
| MAIN-06 | Pontos do vencedor após a vitória | Exatamente 30 (sem ultrapassar) | `req` | RF-06 | ✘ DEF-25 (c no módulo, ver ENV-23); no jogo real a partida encerra em 12 (DEF-02) |
| MAIN-07 | Reinício de mão (`reiniciarJogo`) a partir de estado final | Baralho restante = 34 (40 − 6); mãos novas de 3 cartas; `rodadas=0`; pontos preservados; `truco`/`envido` resetados | `req` | RF-02 | ✔ (p, conferido por leitura: 40 − 6 = 34) |
| MAIN-08 | Entradas esgotadas (EOF) no meio da partida | Encerra com erro controlado | `exc`, `loop` | RNF-02 | ✘ (p) `EOFError` não tratado |
| MAIN-09 | Menu: Truco (`4`) na 1ª rodada e depois `0` | Truco processado e o jogo volta ao menu da mesma rodada | `input_`, `ifs` | RF-20 | ✔ (p) |
| MAIN-10 | Humano escolhe Envido (`6`) quando o bot tem flor | "Bloqueou o envido com a flor"; a Flor é disputada | `ifs`, `msg` | RF-40/41 | ✔ (p) |
| MAIN-11 | Combinação de `if` do turno do humano: (3 cartas?) x (flor do humano?) x (bot pediu flor?) x opção em {5,6,7,8} | Caminho coerente (cantar flor, bloquear envido, envido normal ou inválido) | `ifs` | RF-40/41 | ✔ (p) |

### Ponta a ponta (`tests/test_e2e.py`)

Marcador `e2e` (e `req`) em todos. Executados com baralho armado e CBR *stub*. Distribuição: humano recebe as 3 primeiras `pop()`, bot as 3 seguintes. Siglas: `1E` = 1 de espadas, `1B` = 1 de bastos, `7E`, `7O`, `3C` etc.

UC-23 usa o `Cbr` **real** e pertence ao Gabriel; está listado aqui apenas por completude e não faz parte desta parte.

| ID | Cenário | Resultado esperado | Marcadores | Req. | Status |
|---|---|---|---|---|---|
| UC-01 | Partida completa: semente fixa, humano sempre joga `0` | Termina; um jogador chega ao placar final (30); mensagem de vitória | `e2e`, `req` | RF-01/05 | ✘ DEF-02 |
| UC-02 | Humano vence a mão 2x0: humano `1E,7E,3C` vs bot `4O,5C,6B`; joga `0,0` | +1 ponto ao humano; placar "Pontuação Total" | `e2e`, `req` | RF-14 | ✔ (p) |
| UC-03 | Humano perde 0x2 (cartas invertidas) | Bot +1 | `e2e`, `req` | RF-14 | ✔ (p) |
| UC-04 | 1x1 e a 3ª decide: rodadas V, D, V | Vencedor da 3ª leva a mão | `e2e`, `req` | RF-14 | ✔ (p) |
| UC-05 | 1ª rodada empata (parda), 2ª decide: cartas de mesmo valor na 1ª | Vence quem ganhar a 2ª | `e2e`, `req` | RF-12 | ✘ DEF-03 |
| UC-06 | 2ª rodada empata após 1ª decidida | Vence quem ganhou a 1ª | `e2e`, `req` | RF-12 | ✘ DEF-03 |
| UC-07 | 3ª rodada empata (1x1 e 3ª empatada) | Vence o "mão" | `e2e`, `req` | RF-12 | ✘ DEF-03 |
| UC-08 | Todas as rodadas empatam | Vence o "mão" | `e2e`, `req` | RF-12 | ✘ DEF-03 |
| UC-09 | Humano vai ao baralho (`9`) na 1ª rodada | Bot +1 (valor corrente); nova mão; humano sem pontos | `e2e`, `req` | RF-15 | ✔ (p) |
| UC-10 | Humano canta Truco e o bot recusa (stub `truco` retorna 0) | Humano +1; nova mão; **sem** a mensagem “Jogador … fugiu!” (recusa não é fuga) | `e2e`, `req`, `msg` | RF-20/22 | ✔ (p) nos pontos; ✘ (p) na mensagem: `turno_do_humano` devolve -1 e imprime “Jogador <humano> fugiu!” (candidato a DEF-31, proposto) |
| UC-11 | Truco aceito (stub `truco` retorna 1) e humano vence a mão 2x0 | Humano ganha **2** pontos | `e2e`, `req` | RF-23 | ✘ DEF-04 |
| UC-12 | Escalada completa Truco, Retruco, Vale 4 e humano vence (stub aumenta; humano `'2'`; bot aceita) | Humano ganha **4** pontos | `e2e`, `req` | RF-20/23 | ✔ (p) |
| UC-13 | Envido na 1ª rodada, humano ganha: humano `7E 6E` (33) vs bot 20; entrada `6`; stub de `avaliar_envido` do bot devolve 0 (a confirmar frente a ENV, em que 0 = recusar) | Humano +2 e depois os pontos da mão | `e2e`, `req` | RF-31/32 | ✔ (p) |
| UC-14 | Envido empatado 27 x 27; stub de `avaliar_envido` do bot devolve 0 | Vence o "mão" | `e2e`, `req` | RF-32 | ✘ DEF-07 |
| UC-15 | Envido tentado na 2ª rodada: menu com 2 cartas, entrada `6` | Recusado: "Selecione um valor válido!" | `e2e`, `req`, `msg` | RF-30 | ✔ (p) |
| UC-16 | Falta Envido com placar 5x3: entrada `8`, bot aceita; stub de `avaliar_envido` do bot devolve 0 | Valor = 30 menos os pontos do líder | `e2e`, `req` | RF-34 | ✘ DEF-09 |
| UC-17 | Entradas inválidas em sequência: `abc`, `''`, `99`, `-1`, `3`, depois `0` | Jogo continua e aceita `0` sem encerrar | `e2e`, `input_` | RNF-02 | ✘ DEF-24, DEF-13 |
| UC-18 | Alternância do "mão" em 3 mãos seguidas (humano é mão na 1ª) | 2ª mão: bot é mão; 3ª: humano | `e2e`, `req` | RF-03 | ✘ DEF-21; além disso (p) `__main__.py:171` fixa `jogador1.primeiro=True`, enquanto o requisito §9 prevê mão sorteada (candidato a DEF-32, proposto) |
| UC-19 | Bot com flor (humano sem): baralho armado, bot `7O 4O 5O` | Bot canta flor e ganha **3** antes da 1ª jogada | `e2e`, `req` | RF-41 | ✘ DEF-14 (p) (ramo morto) |
| UC-20 | Humano com flor canta `5`; bot sem flor: humano `1E 7E 5E` (mesmo naipe); stub de `avaliar_envido` do bot devolve 0 | Humano +3; envido anulado | `e2e`, `req` | RF-41 | ✔ (p) |
| UC-21 | Ambos com flor, Contra-flor: `5` do humano; bot aceita | Vencedor pelos pontos de flor; +6 | `e2e`, `req` | RF-42/43 | ✘ DEF-12 |
| UC-22 | Humano recusa Contra-flor | Bot +3 | `e2e`, `req` | RF-42 | ✘ DEF-11 |
| UC-23 | (Gabriel) Partida com `Cbr` real, 5 sementes, humano joga `0` | Nenhuma exceção em toda a partida | `e2e`, `ia` | RF-50 | ✘ DEF-19/17 (p), depende da semente |

### 5.4 RNFs sem dono

Nenhum cenário de `cenarios_de_teste.md` §6 cobre por inteiro estes requisitos não funcionais (a linha "RNF-01…06" aponta apenas para CBR-01b/02/19/21, DAD-14, MAIN-01/08, INT-12/14). Proposta de verificação automatizada, ainda **não especificada** como cenário:

| RNF | O que exige (`requisitos.md` §4) | Como verificar de forma automatizada |
|---|---|---|
| RNF-01 | Python 3; execução por `python -m truco`; dependências em `requirements.txt` (pandas, scikit-learn). | Teste que lê `requirements.txt` e confere `pandas` e `scikit-learn`; `sys.version_info >= (3,)`. O teste de `python -m truco` (`subprocess.run([sys.executable, '-m', 'truco'], input='...')`, esperando o prompt “Nome Jogador 1:”) é `xfail` por DEF-01 e precisa de cwd com a base original, porque `Cbr()` lê o CSV antes do 1º `input`. |
| RNF-03 | Decisão do bot em tempo imperceptível (< 1 s por jogada em hardware comum). | Medir com stub conflita com “CBR sempre stub” (§2). Delegar a medição ao CBR-19 (Gabriel: 20 chamadas de `truco`, `envido` e `jogar_carta`, média < 1 s) ou declarar a exceção e depender da fixture `cbr_real` dele (ainda não existe). Sensível ao hardware: limite com folga e marcador `ia`. A construção do `Cbr()` (≈3 s) fica fora da medida. |
| RNF-04 | Regras (cartas, Truco, Envido, Flor) isoladas da interface e do bot, para permitir testes unitários. | Teste estrutural de import (AST) só vale para `carta`, `baralho`, `pontos`, `truco`, `envido` e `flor`, que não têm imports de `bot`/`cbr`. `jogo.py` importa `bot` (`jogo.py:3`) e `truco.py`, `envido.py`, `flor.py` e `jogo.py` têm `print`/`input`: tratar como `xfail` com DEF-29 (proposto) “regras acopladas a bot e I/O”. Relacionados: DEF-06 e CBR-21 (filtro global de `warnings`). |
| RNF-05 | Cobertura de testes automatizados para hierarquia de cartas, parda, pontos de envido/flor, pontuação de cantos e recusas, fim de partida. | Rodar `pytest --cov=truco --cov-branch --cov-report=term-missing`. `--cov-fail-under=N` fica só no comando de CI, não no `pytest.ini`; N é definido após a 1ª medição (decisão do grupo, a confirmar). Em vez de testar marcadores, usar um checklist de cenários `req` por tema: hierarquia (CAR), parda (UC-05…08), envido/flor (ENV/FLO), recusas (TRU/ENV/FLO), fim de partida (MAIN-05, UC-01). |
| RNF-06 | Base CSV lida com tolerância a erros (arquivo ausente/malformado gera mensagem clara). | `cwd_tmp` sem `dbtrucoimitacao_maos.csv` e sem `modelo_registro.csv`: `Cbr()`/`Dados()` devem dar erro com mensagem clara (hoje `FileNotFoundError` cru, DEF-30 proposto “leitura de CSV sem tratamento de erro”); CSV malformado (colunas faltando, TAB) deve gerar mensagem legível, não `ValueError: Usecols do not match columns` (DEF-01). Sobrepõe CBR-01b, CBR-02 e DAD-14 (Gabriel). `cwd_tmp` e `base_original.csv` ainda não existem (base original: `git show 3b63d88:dbtrucoimitacao_maos.csv`). |

### Observações da interface e E2E (Obs. interface n)

Divergências encontradas ao conferir `truco/*.py` e o documento (nada foi corrigido):

1. `cenarios_de_teste.md` §2 cita "UC-01…UC-20", mas §5 e `status_testes.md` listam UC-01…UC-23.
2. INT-11: `Interface.mostrar_jogador_opcoes` (`truco/interface.py:89-91`) imprime sempre "Jogador 1 é mão" e **nunca é chamado** (o menu usa `Jogador.mostrar_opcoes`, `truco/jogador.py:16`); teste só verifica a função isolada.
3. MAIN-02, entrada `'1,3'`: `int('1,3')` levanta `ValueError` (DEF-24). O DEF-13 cita `1,3` como **duas entradas sucessivas** (`1` e depois `3`) que causam `IndexError`. A grafia ambígua na tabela deve ser esclarecida no teste.
4. `Jogador.mostrar_opcoes` tem efeito colateral: ao exibir o menu com 3 cartas de mesmo naipe, define `self.flor = True` (`truco/jogador.py:23-25`); o `[5] Flor` só aparece na primeira exibição, embora a opção `5` continue válida depois. Não está catalogado (relevante a MAIN-02, MAIN-11 e UC-20).
5. `turno_do_bot` (`truco/__main__.py:125-136`) chama `envido.controlador_envido('Envido', 2, jogador1, jogador2, interface)` com 5 argumentos, mas a assinatura exige 7 (`truco/envido.py:29`): o `TypeError` só ocorre se `Bot.jogar_carta` devolver 6/7/8, o que praticamente não ocorre (BOT-11). Além disso, o ramo `carta_escolhida == 7` (linha 138) é inalcançável quando as flores não foram pedidas. Não catalogado.
6. `__main__.py:40` e `:100`: a condição `int(carta_escolhida) <= 1` do laço de menu faz com que opções `0` e `1` válidas saiam por `break`, mas o critério de repetição é pouco claro (não coberto por cenário).
7. `rodar_main` precisa substituir `Cbr()` por stub antes de `runpy`, pois `__main__.py:155` instancia `Cbr()` na importação e falha com a base TAB (DEF-01).
8. `limpar_tela` em `interface.py` usa `clear` (Linux); em Windows exigiria `cls` (comentado). Não catalogado e vale para INT-14.
9. `requirements.txt` lista só `pandas` e `scikit-learn`, sem `pytest`/`pytest-cov` (também notado em `status_testes.md`; já existe `requirements-dev.txt` não versionado).


## 6. Lacunas nos módulos da Amanda

**Tipo Diátaxis:** referência (catálogo de cenários). Esta seção reúne reforço e variações sobre cenários já descritos, além de lacunas reais; a coluna “Relacionado / duplica” indica o cenário já existente (CAR, JGD, JOG, BAR) ou “Novo”. **Arquivo-alvo:** `tests/test_lacunas.py`. **Oráculo:** `requisitos.md`; onde o código diverge, o teste usa `xfail(strict=True, reason="DEF-nn")`.

Cobre `carta.py`, `pontos.py`, `baralho.py` e `jogador.py`, e só o que o plano de testes da Amanda deixa de fora (ver [`lacunas_plano_testes.md`](lacunas_plano_testes.md), seção 3). Os cenários de `Jogo.verificar_carta_vencedora` aparecem aqui só quando repetem a mesma regra de `Carta`.

Status: `✔ (c)` o código atual passa, confirmado rodando o código em 2026-11-13 · `✘ DEF-nn (c)` o código atual falha, confirmado rodando o código. DEF-26 a DEF-28 são **propostos** nesta revisão (§7).

Execução (da raiz do repositório):

```bash
.venv/bin/python -m pytest tests/test_lacunas.py -v -rxX
```

### 6.1 Manilhas falsas e parda (`carta.py`, `pontos.py`, `jogo.py`)

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-01 | `1C × 12E` e `1O × 12E`, em `verificar_carta_alta` e `verificar_carta_baixa`, nas duas ordens (também em `Jogo.verificar_carta_vencedora`) | o `1` vence; o `12E` é a baixa. Só `1E` e `1B` são manilha | req, call, ret | RF-11 | ✔ (c) | CAR-03/04/05 |
| LAC-02 | `1C × 7O` e `1O × 1B` (falsa contra manilha) | a manilha vence (`7O`, `1B`) | req, call | RF-11 | ✔ (c) | CAR-03/04/05 |
| LAC-03 | `7C × 10O` e `7B × 10O` | o `10O` vence (6 > 4); o `7` é a baixa. Só `7E` e `7O` são manilha | req, call | RF-11 | ✔ (c) | CAR-03/04/05 |
| LAC-04 | `retornar_pontos_carta` para `1C`, `1O`, `7C`, `7B` | `12`, `12`, `4`, `4` (valor da tabela comum, não o de manilha) | call, ret | RF-11 | ✔ (c) | CAR-07 |
| LAC-05 | `3C × 3O` em `Carta.verificar_carta_alta` e `verificar_carta_baixa`, nas duas ordens | parda: o retorno não é nenhuma das duas cartas, e não depende da ordem dos argumentos (representação da parda **a confirmar**) | req, ret | RF-12 | ✘ DEF-03 (c): devolve sempre a 2ª carta | CAR-06 e JOG-02 (idêntico; sugere-se remover da implementação) |
| LAC-06 | `Jogo.verificar_carta_vencedora` com `3C × 3O`, `7C × 7B` e `12E × 12O`, nas duas ordens | parda (como em LAC-05) | req, ret | RF-12 | ✘ DEF-03 (c): devolve sempre a 1ª carta | JOG-02 (idêntico; sugere-se remover da implementação) |

### 6.2 Envido com figura (`jogador.py`, `calcula_envido`)

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-07 | Par do mesmo naipe com uma figura: `12E 3E 4O`, `7E 12E 4O`, `1E 12E 11O` | 23, 27, 21 (`20 + carta`, figura vale 0) | call, ret | RF-32 | ✘ DEF-10 (c): retorna 4, 7, 1 | JGD-05 |
| LAC-08 | Duas figuras do mesmo naipe: `12E 11E 1C`; flor só de figuras: `12E 11E 10E` | 20 e 20 | call, ret | RF-32 | ✘ DEF-10 (c): retorna 1 e 0 | JGD-05 |
| LAC-09 | Figuras sem par de naipe: `12E 12O 5C` | 5 (a maior carta avulsa) | ret | RF-32 | ✔ (c) | JGD-05 |
| LAC-10 | Mão com 2 cartas (`7E 6E`) e mão vazia | 33; mão vazia levanta `ValueError` (`max()` de lista vazia) | exc, loop | RF-32 | ✔ (c) | — (não mapeado; a confirmar) |

### 6.3 Menu do jogador (`jogador.py`, `mostrar_opcoes`, com `capsys`)

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-11 | 3 cartas sem flor (`7E 6O 5E`) | linhas `[0]`, `[1]`, `[2]`, `[4] Truco`, `[6]`, `[7]`, `[8]`, `[9]`; sem `[5]` | ifs, msg | RF-20, 30 | ✔ (c) | JGD-07 |
| LAC-12 | 3 cartas com flor (`7E 6E 5E`), 1ª chamada | aparece `[5] Flor` | ifs, msg | RF-40 | ✔ (c) | JGD-07 |
| LAC-13 | A mesma mão, 2ª chamada | `[5] Flor` continua aparecendo | ifs, msg | RF-40 | ✘ DEF-26 (c): a 1ª chamada liga `flor=True` e a opção some | JGD-08 |
| LAC-14 | Mão de flor recém-criada por `criar_mao` (`5E 6E 7E`) | `flor is True` antes de qualquer menu | req | RF-40 | ✘ DEF-26 (c): `flor` fica `False` e `checa_flor()` dá `True` | Novo (detalhe de implementação; sintoma real é LAC-13, ou fundir) |
| LAC-15 | 2 cartas; 2 cartas com `pediu_truco`; 1 carta; 0 cartas | `[4]` e `[9]` / só `[9]` com cartas / `[0]` e `[9]` / só `[9]`; nunca `[5]`, `[6]`, `[7]`, `[8]` | ifs, msg, loop | RF-20, 30 | ✔ (c) | JGD-07 |

### 6.4 Entradas inexistentes

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-16 | `retornar_pontos_envido` com carta de número 8 e 9 | `KeyError` | exc | RF-32 | ✔ (c) | CAR-13 |
| LAC-17 | `retornar_pontos_carta` e `verificar_carta_alta` com carta de número 8 ou 9 | `KeyError` | exc | RF-02 | ✔ (c) | CAR-16 |
| LAC-18 | `retornar_naipe_codificado` com `"PAUS"` e `"copas"` (minúsculo) | `None` | call, ret | RF-54 | ✔ (c) | CAR-14 (só “copas” minúsculo é novo) |
| LAC-19 | `classificar_carta` com lista de 2 e de 0 cartas | `IndexError` | exc | RF-50 | ✔ (c) | CAR-10 |
| LAC-20 | `jogar_carta(3)`; `jogar_carta("x")`; `jogar_carta(None)`; `jogar_carta(-1)` | `IndexError`; `TypeError`; `TypeError`; devolve a última carta (registrar) | exc, call | RF-10 | ✔ (c) | JGD-04 |
| LAC-21 | `criar_mao` com baralho de 2 cartas | `IndexError`; a mão fica com 2 cartas, `envido == 0` e baralho vazio (estado parcial, registrar) | exc, loop | RF-02 | ✔ (c) | JOG-08 |
| LAC-22 | `retirar_carta` depois de `resetar()` | `IndexError` | exc | RF-02 | ✔ (c) | Novo |

### 6.5 Saída de tela (`capsys`)

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-23 | `exibir_carta()` e `exibir_carta(0)` com `3 de OUROS` | `[] 3 de OUROS` e `[0] 3 de OUROS` (sem espaço dentro do `[]`) | msg | RNF-02 | ✔ (c) | CAR-11 |
| LAC-24 | `printar_baralho` num baralho novo; depois de `resetar()` | 40 linhas, da primeira `[] 1 de ESPADAS` à última `[] 12 de BASTOS`; saída vazia depois de `resetar()` | msg, loop | RNF-02 | ✔ (c) | BAR-09 |

### 6.6 Baralho

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-25 | `random.seed(7)` + `embaralhar()` duas vezes; `seed(8)`; comparação com a ordem original | mesma permutação com a mesma semente; semente diferente dá outra; mesmo conjunto de 40 cartas; ordem diferente da original | req, call | RF-02 | ✔ (c) | BAR-04 |
| LAC-26 | Baralho novo | 40 pares (número, naipe) únicos; 10 por naipe; números `{1..7, 10, 11, 12}` | req, loop | RF-02 | ✔ (c) | BAR-01/02/03 |
| LAC-27 | Distribuir 3 cartas ao humano e 3 ao bot (`criar_mao` duas vezes) | 6 cartas distintas, 34 restantes, nenhuma das 6 no baralho | req | RF-02 | ✔ (c) | BAR-07 |
| LAC-28 | `criar_baralho()` chamado 2 vezes seguidas | 80 cartas, só 40 únicas (duplica; registrar o comportamento, **a confirmar** se é defeito) | call, ret | RF-02 | ✔ (c) | BAR-08 |
| LAC-29 | `resetar()` e depois `criar_baralho()` | 0 cartas e `manilhas == []`; depois 40 | call, req | RF-02 | ✔ (c) | BAR-08 |

### 6.7 Esconder carta e classificação

| ID | Cenário | Esperado | Marcadores | Req. | Status | Relacionado / duplica |
|---|---|---|---|---|---|---|
| LAC-30 | Menu com 3 cartas: o jogador pode escolher jogar uma carta escondida | `mostrar_opcoes` oferece a opção e `jogar_carta` aceita jogar escondida (formato da opção e do retorno **a confirmar**, o requisito não os define) | req, msg | RF-10 | ✘ DEF-27 (c): não há método, opção nem texto de "esconder" em `truco/` | Novo |
| LAC-31 | `classificar_carta([3C, 3O, 3B])` (três valores iguais) | exatamente uma `Alta`, uma `Media` e uma `Baixa` | ret | RF-50 | ✘ DEF-28 (c): retorna `['Media','Media','Baixa']`, sem `Alta` | Novo |

---

## 7. Tabela de defeitos (módulos jogo, truco, envido, flor, interface, main e lacunas)

Extraída do catálogo da seção 3 de [`cenarios_de_teste.md`](cenarios_de_teste.md), só com o que importa a esses módulos. DEF-14 a DEF-17, 19, 20 e 22 (bot, CBR, dados) ficam de fora; DEF-14, 17 e 19: ver catálogo §3 (Gabriel). DEF-26 a DEF-30 são propostos. A coluna "Comportamento real" repete a evidência do catálogo (marcada `(c)` ali) e, nos DEF-10, 26, 27 e 28, a confirmada nesta revisão.

| DEF | Requisito violado | Comportamento real | Cenários que o expõem |
|---|---|---|---|
| DEF-01 | RNF-01, RNF-06, RF-52 | `Cbr()` não inicia: o CSV da base está separado por TAB e o código lê com vírgula (`ValueError: Usecols do not match columns`). O `__main__` depende do `Cbr` | UC-23 e os cenários de `__main__` que usam CBR real |
| DEF-02 | RF-01, RF-05 | A partida termina com 12 pontos (`>= 12`) e a falta usa `12 − pontos` | MAIN-05, UC-01 |
| DEF-03 | RF-12, RF-13 | Não existe parda: o empate de carta devolve a 1ª carta (`Jogo`) ou a 2ª (`Carta`) | LAC-05, LAC-06, CAR-06, JOG-02, UC-05 a UC-08 |
| DEF-04 | RF-23 | Truco aceito não muda o valor da mão (continua 1) | TRU-02, UC-11 |
| DEF-05 | RF-21 | `estado_atual` nunca vira `vale_quatro`; depois do Vale 4, um novo canto baixa a aposta de 4 para 3 | TRU-09, TRU-17, TRU-18 |
| DEF-06 | RNF-04 | `retornar_quem_fugiu()` devolve o próprio método, não um jogador | TRU-13 |
| DEF-07 | RF-32 | Empate de envido favorece sempre o jogador 1 (`>=`), não o "mão" | ENV-04, UC-14 |
| DEF-08 | RF-31, RF-33 | Real Envido direto vale 5 (requisito: 3) e, recusado, dá 2 (requisito: 1) | ENV-07, ENV-08 |
| DEF-09 | RF-33, RF-34 | Falta Envido = `12 − pontos do adversário do cantor`; recusa fixa em 5 | ENV-10, ENV-11, ENV-12, UC-16 |
| DEF-10 | RF-32 | `calcula_envido` zera o par do mesmo naipe com figura: `12E 3E 4O` retorna 4 (esperado 23), `7E 12E 4O` retorna 7 (27), `12E 11E 10E` retorna 0 (20). O Bot tem a mesma regra (a confirmar rodando) | JGD-05, LAC-07, LAC-08 |
| DEF-11 | RF-42 | Recusa da Contra-flor concede 4 pontos (requisito: 3) | FLO-05, UC-22 |
| DEF-12 | RF-42, RF-43 | "Contra-flor e o resto" não soma a falta (valor 3); o vencedor da flor sai dos pontos de envido (par), não das 3 cartas (`7E 6E 5E` dá 33, não 38) | FLO-04, FLO-06, UC-21 |
| DEF-13 | RF-10, RNF-02 | Opção igual ao número de cartas (3 com 3 cartas, 2 com 2, 1 com 1) chama `pop()` fora do intervalo: `IndexError` | MAIN-02, MAIN-03, MAIN-04 (opção `1` com 1 carta), UC-17 |
| DEF-18 | RNF-02 | Saídas de depuração (`print(1)` a `print(4)`) poluem o terminal | ENV-21 |
| DEF-21 | RF-03 | O "mão" não alterna: `quem_inicia_rodada` nunca é chamado pelo `__main__` | JOG-10, UC-18 |
| DEF-23 | RF-04 (catálogo §3); RF-32 e RF-41 vêm dos cenários, divergência a confirmar | `mostrar_vencedor_flor` e `mostrar_vencedor_envido` tratam qualquer vencedor diferente de 1 como “Jogador 2” (inclui 0) | ENV-15 (tipo 5, 9 e −1; o 0 passa), FLO-03, INT-07, INT-09 |
| DEF-24 | RNF-02 | Entradas não numéricas (`'abc'`, `''`, `'0.5'`) em qualquer menu levantam `ValueError` | TRU-12, ENV-16, FLO-10, MAIN-02, UC-17 |
| DEF-25 | RF-06 | Os pontos passam do placar final: no módulo, 29 pts + envido/flor dão 31, sem teto (c, ENV-23). No jogo real a partida encerra em 12 (DEF-02), então o limite 30 só vale ao corrigir DEF-02 | ENV-23, MAIN-06 |
| DEF-26 *(proposto)* | RF-40 | `Jogador.flor` só vira `True` como efeito colateral de `mostrar_opcoes`, e a opção `[5] Flor` some na 2ª chamada (`criar_mao` não liga `flor`, ao contrário do `Bot`) | LAC-13, LAC-14, JGD-08 |
| DEF-27 *(proposto)* | RF-10 | Não existe a opção de jogar a carta escondida (nenhum método, texto ou ramo em `truco/`) | LAC-30 |
| DEF-28 *(proposto)* | RF-50 | `classificar_carta` com 3 cartas de mesmo valor não devolve `Alta` (o rótulo `Baixa` sobrescreve) | LAC-31 (CAR-09 é relacionado e passa) |
| DEF-29 *(proposto)* | RNF-04 | Regras acopladas a bot e I/O: `jogo.py` importa `bot` (`jogo.py:3`); `truco.py`, `envido.py`, `flor.py` e `jogo.py` têm `print`/`input` | RNF-04 (teste de import, `xfail`) |
| DEF-30 *(proposto)* | RNF-06 | Leitura de CSV sem tratamento de erro: arquivo ausente ou malformado propaga exceção crua | RNF-06 (sobrepõe CBR-01b, CBR-02 e DAD-14, do Gabriel) |

---

## 8. Observações das lacunas e defeitos (Obs. lacunas n)

1. **Verificação:** todos os status foram conferidos rodando o código com `.venv/bin/python` a partir da raiz, com `PYTHONPATH=.` (sem ele, `import truco` falha fora do pytest). Nada no repositório foi alterado. O DEF-25 e a nota do Bot em DEF-10 não foram reexecutados: vêm do catálogo ("previsto").
2. **Divergência de formato na documentação:** `exibir_carta()` imprime `[] 3 de OUROS` (sem espaço), mas CAR-11 e BAR-09 em `cenarios_de_teste.md` esperam `[ ] 3 de OUROS`. Os cenários LAC-23 e LAC-24 usam o formato real. Corrigir CAR-11 e BAR-09 é decisão de quem mantém esse arquivo.
3. **Parda:** o `requisitos.md` não define como o código deve representar a parda (retorno `None`, string, etc.). Por isso LAC-05 e LAC-06 afirmam só "não é nenhuma das duas cartas" (os dois duplicam CAR-06 e JOG-02: sugere-se removê-los da implementação para não duplicar `xfail`). **A confirmar** com o grupo antes de endurecer o oráculo.
4. **Esconder carta (RF-10):** o requisito não detalha o fluxo; LAC-30 fica como `xfail` genérico até alguém definir a opção de menu.
5. **DEF-26 propõe uma causa só para dois sintomas** (opção que some e `flor` ligada pelo menu). Se o grupo preferir, dá para separar em dois DEF. Atenção: o `__main__` (linha 65) só aceita a opção `5` se `jogador1.flor` já foi ligado por um menu, e `flor.py:25` lê `jogador1.flor`.
6. **Bot:** o `Bot.calcula_envido` e `Bot.checa_flor` não foram escopo desta parte; o DEF-10 diz que o Bot tem a mesma falha, mas isso não foi reexecutado aqui.
7. **Candidatos a DEF novos** (não incluídos na tabela do §7; numeração sugerida, todos *(proposto)*): DEF-31 recusa de truco pelo bot faz `turno_do_humano` devolver -1 e imprimir “Jogador <humano> fugiu!” (UC-10, p); DEF-32 mão não sorteada, pois `__main__.py:171` fixa `jogador1.primeiro=True` e o requisito §9 prevê sorteio (UC-18, p); DEF-33 `jogador_fugiu` sempre define j1 como mão e é código morto (JOG-07, c); DEF-34 `controlador_truco` no estado `retruco` chama `pedir_retruco` de novo (TRU-17, c). Sem numeração sugerida (a decidir): FLO-07, FLO-12, INT-11, MAIN-01, MAIN-08 e a parte do `4` em MAIN-04. ENV-20 saiu da lista: passa (c).
8. **Nome do rótulo:** `classificar_carta` devolve `'Media'` sem acento; o CT-CAR-09 do plano da Amanda espera "Média". Os testes de LAC-31 comparam com o valor real `'Media'`.
9. **Estrutura:** dependem da fixture `mk` (`tests/conftest.py`) para criar cartas por código (`mk('3C')`); `Jogador.flor` e `calcula_envido` são testados sem monkeypatch. LAC-11 a LAC-15 e LAC-23 a LAC-24 usam `capsys`.
10. **Skill:** não invoquei a skill `documentation-writer`; o documento é só uma tabela de referência.
