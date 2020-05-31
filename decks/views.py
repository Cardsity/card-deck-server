from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import SingleObjectMixin
from .models import Deck


class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello world!")


class DeckJSONView(SingleObjectMixin, View):
    """Returns a deck as a json."""
    model = Deck

    def get(self, request, *args, **kwargs):
        # Return the deck as a json
        return JsonResponse(self.get_object().as_dict())
