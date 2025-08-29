import random
from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import F

from .models import Quote
from .exceptions import DuplicateQuoteError, SourceLimitError


class QuoteService:
    @staticmethod
    def add_quote(text, source, weight=1.0):
        max_per_source = getattr(settings, 'MAX_QUOTES_PER_SOURCE', 3)
        current = Quote.objects.filter(source=source).count()
        if current >= int(max_per_source):
            raise SourceLimitError(f"Source '{source}' reached limit of {max_per_source} quotes")

        try:
            with transaction.atomic():
                q = Quote.objects.create(text=text, source=source, weight=weight)
                return q
        except IntegrityError as e:
            raise DuplicateQuoteError('Quote with same text and source already exists') from e

    @staticmethod
    def get_weighted_random():
        qs = Quote.objects.all().values_list('id', 'weight')
        items = list(qs)
        if not items:
            return None
        ids, weights = zip(*items)
        chosen_id = random.choices(ids, weights=weights, k=1)[0]
        return Quote.objects.filter(pk=chosen_id).first()

    @staticmethod
    def increment_view(quote_id, by=1):
        Quote.objects.filter(pk=quote_id).update(views=F('views') + by)
        q = Quote.objects.filter(pk=quote_id).first()
        return q.views if q else None

    @staticmethod
    def like(quote_id):
        Quote.objects.filter(pk=quote_id).update(likes=F('likes') + 1)
        q = Quote.objects.filter(pk=quote_id).first()
        return (q.likes, q.dislikes) if q else (None, None)

    @staticmethod
    def dislike(quote_id):
        Quote.objects.filter(pk=quote_id).update(dislikes=F('dislikes') + 1)
        q = Quote.objects.filter(pk=quote_id).first()
        return (q.likes, q.dislikes) if q else (None, None)

