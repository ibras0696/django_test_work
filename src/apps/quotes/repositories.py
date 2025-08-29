from django.db import IntegrityError
from .models import Quote


class QuoteRepository:
    @staticmethod
    def create_quote(text, source, weight=1.0):
        try:
            q = Quote.objects.create(text=text, source=source, weight=weight)
            return q
        except IntegrityError as e:
            # Raise a clearer exception for unique constraint
            raise IntegrityError('Quote with the same text and source already exists') from e

    @staticmethod
    def get_by_id(pk):
        return Quote.objects.filter(pk=pk).first()

    @staticmethod
    def list_all():
        return Quote.objects.all()

    @staticmethod
    def filter_by_source(source):
        return Quote.objects.filter(source=source)

    @staticmethod
    def top_by_likes(limit=10):
        return Quote.objects.order_by('-likes')[:limit]
