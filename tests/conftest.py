"""Fixtures compartilhadas. Acrescente aqui; evite editar o que já existe."""
import pytest

from truco.carta import Carta


def carta(codigo):
    """'3C' -> Carta(3, 'COPAS'); '12E' -> Carta(12, 'ESPADAS')."""
    naipes = {"E": "ESPADAS", "O": "OUROS", "C": "COPAS", "B": "BASTOS"}
    return Carta(int(codigo[:-1]), naipes[codigo[-1]])


@pytest.fixture
def mk():
    """Fábrica de cartas a partir de códigos curtos (ex.: mk('1E'))."""
    return carta
