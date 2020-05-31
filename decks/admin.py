from django.contrib import admin
from .models import Deck, BlackCard, WhiteCard


class BlackCardInline(admin.TabularInline):
    """Tabular inline for black cards."""
    model = BlackCard
    fk_name = "deck"


class WhiteCardInline(admin.TabularInline):
    """Tabular inline for white cards."""
    model = WhiteCard
    fk_name = "deck"


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    """The deck admin site."""
    list_display = ('pk', 'name')
    inlines = (BlackCardInline, WhiteCardInline)
