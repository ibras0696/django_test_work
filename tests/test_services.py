import math
import pytest
from apps.quotes.services import QuoteService
from apps.quotes.repositories import QuoteRepository
from apps.quotes.models import Quote


def test_add_quote_and_constraints(db, settings):
    settings.MAX_QUOTES_PER_SOURCE = 3
    q1 = QuoteService.add_quote('s1', 'srcA')
    assert q1.pk

    # duplicate
    with pytest.raises(Exception):
        QuoteService.add_quote('s1', 'srcA')

    # limit
    QuoteService.add_quote('s2', 'srcA')
    QuoteService.add_quote('s3', 'srcA')
    with pytest.raises(Exception):
        QuoteService.add_quote('s4', 'srcA')


def test_weighted_random_statistical(db):
    Quote.objects.all().delete()
    # create 3 quotes with weights 1,2,7 => probabilities 0.1,0.2,0.7
    q1 = QuoteRepository.create_quote('w1', 'ws')
    q1.weight = 1.0; q1.save()
    q2 = QuoteRepository.create_quote('w2', 'ws')
    q2.weight = 2.0; q2.save()
    q3 = QuoteRepository.create_quote('w3', 'ws')
    q3.weight = 7.0; q3.save()

    counts = {q1.id: 0, q2.id: 0, q3.id: 0}
    N = 10000
    for _ in range(N):
        chosen = QuoteService.get_weighted_random()
        counts[chosen.id] += 1

    freqs = [counts[q1.id]/N, counts[q2.id]/N, counts[q3.id]/N]
    expected = [0.1, 0.2, 0.7]

    # allow 4 sigma tolerance where sigma = sqrt(p(1-p)/N)
    for f, p in zip(freqs, expected):
        sigma = math.sqrt(p*(1-p)/N)
        assert abs(f-p) <= 4*sigma


def test_atomic_increments(db):
    q = QuoteRepository.create_quote('inc', 'incsrc')
    assert q.views == 0
    QuoteService.increment_view(q.id)
    q.refresh_from_db()
    assert q.views == 1
    QuoteService.like(q.id)
    q.refresh_from_db()
    assert q.likes == 1
    QuoteService.dislike(q.id)
    q.refresh_from_db()
    assert q.dislikes == 1
