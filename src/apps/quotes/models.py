from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import F


class Quote(models.Model):
    text = models.TextField()
    source = models.CharField(max_length=255)
    weight = models.FloatField(default=1.0, validators=[MinValueValidator(0.000001)])
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # UniqueConstraint to be enforced: (text, source)
        constraints = [
            models.UniqueConstraint(fields=['text', 'source'], name='unique_text_source')
        ]
        # index on likes descending
        indexes = [
            models.Index(F('likes').desc(), name='likes_desc')
        ]

    def __str__(self):
        return f"{self.text[:50]}... - {self.source}"

    def increment_views(self, by=1):
        # to be used with update(F(...)) in service layer for atomic increments
        self.views = F('views') + by
        self.save(update_fields=['views'])
