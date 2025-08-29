from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.random_view, name='quotes-random'),
    path('top/', views.top_view, name='quotes-top'),
    path('add/', views.add_view, name='quotes-add'),
    path('like/<int:quote_id>/', views.like, name='quotes-like'),
    path('dislike/<int:quote_id>/', views.dislike, name='quotes-dislike'),
    path('', views.random_view, name='quotes-index'),
]
