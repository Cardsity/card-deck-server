from django.views.generic.base import View
from django.http import JsonResponse
from .models import News


class NewsListJSONView(View):
    """Returns all news as json."""
    def get(self, request):
        # TODO: Add pagination
        # Get all news as a dict
        news_dict = News.get_all_news_as_dict()
        # Return the news as a json
        return JsonResponse(news_dict)
