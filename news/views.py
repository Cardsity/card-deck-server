from django.views.generic.base import View
from django.views.generic.list import ListView
from django.http import JsonResponse
from .models import News


class NewsListView(ListView):
    """Renders all news."""
    model = News
    paginate_by = 5
    template_name = "news/list.html"


class NewsListJSONView(View):
    """Returns all news as json."""
    def get(self, request):
        # TODO: Add pagination
        # Get all news as a dict
        news_dict = News.get_all_news_as_dict()
        # Return the news as a json
        return JsonResponse(news_dict)
