from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .services import QuoteService
from .exceptions import DuplicateQuoteError, SourceLimitError


def random_view(request):
    # GET: show weighted random quote and increment view
    q = QuoteService.get_weighted_random()
    if not q:
        return render(request, 'quotes/random.html', {'quote': None})

    # increment view atomically
    QuoteService.increment_view(q.id)
    # reload to get updated views
    q = q.__class__.objects.filter(pk=q.id).first()
    return render(request, 'quotes/random.html', {'quote': q})


def top_view(request):
    qs = QuoteService.__class__  # placeholder to avoid lint; we'll call repository via model
    from .repositories import QuoteRepository
    top = QuoteRepository.top_by_likes(10)
    return render(request, 'quotes/top.html', {'quotes': top})


@csrf_exempt  # TEMP: disable CSRF for this view while demoing via ngrok; remove for production
def add_view(request):
    errors = []
    data = {'text': '', 'source': '', 'weight': '1.0'}
    if request.method == 'POST':
        data['text'] = request.POST.get('text', '').strip()
        data['source'] = request.POST.get('source', '').strip()
        data['weight'] = request.POST.get('weight', '1.0').strip()

        if not data['text']:
            errors.append('Требуется текст')
        if not data['source']:
            errors.append('Требуется источник')

        try:
            weight_val = float(data['weight'])
            if weight_val <= 0:
                errors.append('Вес должен быть положительным')
        except ValueError:
            errors.append('Вес должен быть числом')

        if not errors:
            try:
                q = QuoteService.add_quote(data['text'], data['source'], weight=float(data['weight']))
                return redirect(reverse('quotes-top'))
            except SourceLimitError as e:
                errors.append(str(e))
            except DuplicateQuoteError as e:
                errors.append(str(e))

    return render(request, 'quotes/add.html', {'errors': errors, 'data': data})


@csrf_exempt  # TEMP: allow likes from public demo
def like(request, quote_id):
    if request.method == 'POST':
        QuoteService.like(quote_id)
    return redirect(request.META.get('HTTP_REFERER', reverse('quotes-random')))


@csrf_exempt  # TEMP: allow dislikes from public demo
def dislike(request, quote_id):
    if request.method == 'POST':
        QuoteService.dislike(quote_id)
    return redirect(request.META.get('HTTP_REFERER', reverse('quotes-random')))

