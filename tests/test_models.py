import pytest
from apps.quotes.models import Quote
from apps.quotes.repositories import QuoteRepository


def test_create_quote(db):
    q = QuoteRepository.create_quote('text1', 'src1')
    assert q.pk is not None


def test_duplicate_quote_raises(db):
    QuoteRepository.create_quote('dup', 'srcx')
    with pytest.raises(Exception):
        QuoteRepository.create_quote('dup', 'srcx')


def test_max_quotes_per_source(db, settings):
    settings.MAX_QUOTES_PER_SOURCE = 3
    for i in range(3):
        QuoteRepository.create_quote(f't{i}', 'src_lim')
    with pytest.raises(Exception):
        QuoteRepository.create_quote('t3', 'src_lim')
