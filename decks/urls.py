from django.urls import path

from . import views

app_name = 'decks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('deck/<int:pk>/json/', views.DeckJSONView.as_view(), name='deck_as_json'),
    path('deck/add/', views.DeckAddView.as_view(), name='deck_add'),
    path('deck/list/', views.DeckListView.as_view(), name='deck_list'),
    path('deck/list/json/', views.DeckListJSONView.as_view(), name='deck_list_as_json'),
    path('deck/<int:pk>/', views.DeckDetailView.as_view(), name='deck_detail'),
]
