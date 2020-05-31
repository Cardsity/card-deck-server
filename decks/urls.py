from django.urls import path

from . import views

app_name = 'decks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('deck/<int:pk>/json/', views.DeckJSONView.as_view(), name='deck_as_json'),
    path('deck/list/', views.DeckListView.as_view(), name='deck_list'),
]
