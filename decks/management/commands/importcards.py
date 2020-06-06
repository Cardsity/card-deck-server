from django.core.management.base import BaseCommand, CommandError
from decks.models import Deck, BlackCard, WhiteCard
import requests
import re

# A regex to match urls
# See https://urlregex.com/
URL_REGEX = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class Command(BaseCommand):
    """
    A command to import cards into a new deck.
    TODO: Write tests
    """
    help = 'Imports cards as a deck.'

    def add_arguments(self, parser):
        parser.add_argument('--url', '-u', required=True, dest='url', help='The url to process.')
        parser.add_argument('--name', required=True, dest='name', help='The name of the deck.')
        parser.add_argument('--official', action='store_true', dest='official',
                            help='If the deck should be an official deck.')

    def handle(self, *args, **options):
        # Check if the supplied url is a valid url
        if not URL_REGEX.match(options["url"]):
            raise CommandError("The supplied url is not a valid url.")

        # Fetch the url
        r = None
        try:
            r = requests.get(options['url'])
        except:
            raise CommandError("Could not get fetch the url.")

        # Check if the request was successful
        if r.status_code != 200:
            raise CommandError("The server returned the status code %s." % r.status_code)

        # Check if the data is valid (only regarding the )
        data = r.json()
        if ("black_cards" not in data) or ("white_cards" not in data):
            raise CommandError("The json data is invalid.")

        # Create the deck
        deck = Deck.objects.create(name=options["name"], official=options["official"])

        # Create the cards
        # NOTE: We can't use bulk create because we need to call the save() method
        for black_card in data["black_cards"]:
            BlackCard.objects.create(deck=deck, text=black_card)
        for white_card in data["white_cards"]:
            WhiteCard.objects.create(deck=deck, text=white_card)

        self.stdout.write(self.style.SUCCESS("Successfully created the {official}deck '{deck_name}' with "
                                             "{black_card_count} black cards and {white_card_count} "
                                             "white cards!".format(official="official " if options["official"] else "",
                                                                   deck_name=deck.name,
                                                                   black_card_count=deck.blackcard_set.count(),
                                                                   white_card_count=deck.whitecard_set.count())))
