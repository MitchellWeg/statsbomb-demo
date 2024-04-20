from statsbomb_demo.helpers import clean_str
import pytest


def test_quote():
    a = "Australian Women's"
    b = "Australian Women''s"
    cleaned = clean_str(a)

    assert cleaned == b


def test_quote_harder():
    a = "Côte d'Ivoire"
    b = "Côte d''Ivoire"
    cleaned = clean_str(a)

    assert cleaned == b
