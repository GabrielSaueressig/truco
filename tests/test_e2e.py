"""Ponta a ponta (__main__.py) — casos principais: UC-02, 03, 05, 09, 10, 11 e 13.

`rodar_main` executa o `truco/__main__.py` de verdade com:
  * baralho armado (humano recebe as 3 primeiras cartas, bot as 3 seguintes);
  * CBR e Dados falsos (sem ler CSV, sem depender do trabalho do Gabriel);
  * roteiro de entradas; quando acaba, levanta EOFError e a execução para,
    com o estado dos jogadores já capturado.
"""
import runpy

import pytest

NAIPES = {"E": "ESPADAS", "O": "OUROS", "C": "COPAS", "B": "BASTOS"}


class CbrFalso:
    """Stub: `truco` e `envido` seguem filas; sem fila, o bot não canta nem aceita."""

    def __init__(self, truco=(), envido=()):
        self._truco = list(truco)
        self._envido = list(envido)

    def flor(self):
        return False

    def truco(self, tipo, quem_pediu, qualidade):
        return self._truco.pop(0) if self._truco else None

    def envido(self, tipo, quem_pediu, pontos, perdendo):
        return self._envido.pop(0) if self._envido else 0

    def jogar_carta(self, rodada, pontuacao_cartas):
        return 0


class DadosFalso:
    def __getattr__(self, nome):
        return lambda *a, **k: None


@pytest.fixture
def rodar_main(monkeypatch):
    def _rodar(deck, entradas, truco=(), envido=()):
        """deck = ['1E','7E','3C','4O','5C','6B']: 3 do humano, depois 3 do bot."""
        fila = list(entradas)

        def entrada(*_a, **_k):
            if not fila:
                raise EOFError
            return fila.pop(0)

        def embaralhar(lista):
            desejadas = []
            for codigo in deck:
                for c in lista:
                    if (c.numero, c.naipe) == (int(codigo[:-1]), NAIPES[codigo[-1]]):
                        desejadas.append(c)
            resto = [c for c in lista if c not in desejadas]
            lista[:] = resto + desejadas[::-1]  # pop() tira na ordem de `deck`

        from truco.jogo import Jogo

        criados = []
        for nome in ("criar_jogador", "criar_bot"):
            original = getattr(Jogo, nome)

            def embrulho(self, *a, _o=original, **k):
                j = _o(self, *a, **k)
                criados.append(j)
                return j

            monkeypatch.setattr(Jogo, nome, embrulho)

        monkeypatch.setattr("builtins.input", entrada)
        monkeypatch.setattr("random.shuffle", embaralhar)
        monkeypatch.setattr("truco.cbr.Cbr", lambda: CbrFalso(truco, envido))
        monkeypatch.setattr("truco.dados.Dados", DadosFalso)
        with pytest.raises(EOFError):
            runpy.run_module("truco.__main__", run_name="__main__")
        humano, bot = criados
        return humano, bot

    return _rodar


NOMES = ["Ana", "Bot"]


# UC-02 — RF-14: humano vence a mão 2x0
@pytest.mark.e2e
@pytest.mark.req
def test_uc02_humano_vence_a_mao(rodar_main):
    humano, bot = rodar_main(["1E", "7E", "3C", "4O", "5C", "6B"], NOMES + ["0", "0"])
    assert (humano.pontos, bot.pontos) == (1, 0)


# UC-03 — RF-14: humano perde 0x2
@pytest.mark.e2e
@pytest.mark.req
def test_uc03_humano_perde_a_mao(rodar_main):
    humano, bot = rodar_main(["4O", "5C", "6B", "1E", "7E", "3C"], NOMES + ["0", "0"])
    assert (humano.pontos, bot.pontos) == (0, 1)


# UC-05 — RF-12: 1ª rodada empata (3C x 3O), a 2ª decide (bot ganha com 5B x 4O)
# Esperado: bot vence a mão. Hoje o empate vira vitória do humano e a 3ª rodada o favorece.
@pytest.mark.e2e
@pytest.mark.req
@pytest.mark.xfail(strict=True, reason="DEF-03: empate de cartas não vira parda")
def test_uc05_parda_na_primeira_rodada(rodar_main):
    humano, bot = rodar_main(["3C", "4O", "7E", "3O", "5B", "6B"], NOMES + ["0", "0", "0"])
    assert (humano.pontos, bot.pontos) == (0, 1)


# UC-09 — RF-15: humano vai ao baralho na 1ª rodada
@pytest.mark.e2e
@pytest.mark.req
def test_uc09_humano_vai_ao_baralho(rodar_main):
    humano, bot = rodar_main(["1E", "7E", "3C", "4O", "5C", "6B"], NOMES + ["9"])
    assert (humano.pontos, bot.pontos) == (0, 1)


# UC-10 — RF-20/22: truco recusado pelo bot dá 1 ponto ao humano
@pytest.mark.e2e
@pytest.mark.req
def test_uc10_truco_recusado(rodar_main):
    humano, bot = rodar_main(["4O", "5C", "6B", "1E", "7E", "3C"], NOMES + ["4"], truco=[0])
    assert (humano.pontos, bot.pontos) == (1, 0)


# UC-11 — RF-23: truco aceito e humano vence 2x0: vale 2 pontos
@pytest.mark.e2e
@pytest.mark.req
@pytest.mark.xfail(strict=True, reason="DEF-04: valor da mão não sobe para 2")
def test_uc11_truco_aceito_vale_dois(rodar_main):
    humano, bot = rodar_main(
        ["1E", "7E", "3C", "4O", "5C", "6B"], NOMES + ["4", "0", "0"], truco=[1]
    )
    assert (humano.pontos, bot.pontos) == (2, 0)


# UC-13 — RF-31/32: envido na 1ª rodada; humano 7E 6E (33) x bot 20; bot aceita
# envido = [0 (checagem inicial do bot), 1 (resposta ao canto do humano)]
@pytest.mark.e2e
@pytest.mark.req
def test_uc13_envido_do_humano_vence(rodar_main):
    humano, bot = rodar_main(
        ["7E", "6E", "4O", "5C", "4B", "3O"], NOMES + ["6", "0", "0"], envido=[0, 1]
    )
    assert (humano.pontos, bot.pontos) == (2 + 1, 0)
