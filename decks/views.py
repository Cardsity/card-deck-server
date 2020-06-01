from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .models import Deck, BlackCard, WhiteCard
from .forms import DeckAddForm
from django.shortcuts import redirect


class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello world!")


class DeckAddView(FormView):
    """Adds a new deck."""
    template_name = 'decks/deck_add.html'
    form_class = DeckAddForm
    success_url = 'decks:deck_detail'

    def form_valid(self, form):
        """Adds a new deck."""
        # Create a new deck
        deck = Deck.objects.create(name=form.cleaned_data["name"])

        # NOTE: We need to call the create method for every card (= no bulk create) so the save() method will be called
        # Create the black cards
        for card in form.cleaned_data["card_json"]["black_cards"]:
            BlackCard.objects.create(deck=deck, text=card)
        # Create the white cards
        for card in form.cleaned_data["card_json"]["white_cards"]:
            WhiteCard.objects.create(deck=deck, text=card)

        # Redirect
        return redirect(self.success_url, pk=deck.pk)


class DeckListView(ListView):
    """Shows all decks."""
    model = Deck
    template_name = 'decks/list.html'
    paginate_by = 20


class DeckDetailView(DetailView):
    """Shows information about a specific deck."""
    model = Deck
    template_name = 'decks/deck_detail.html'


class DeckJSONView(SingleObjectMixin, View):
    """Returns a deck as a json."""
    model = Deck

    def get(self, request, *args, **kwargs):
        # Return the deck as a json
        return JsonResponse(self.get_object().as_dict())
