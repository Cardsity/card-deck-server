from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('list/json/', views.NewsListJSONView.as_view(), name='list_as_json'),
]
