from django.core.management.base import BaseCommand, CommandError
from decks.models import Deck, BlackCard, WhiteCard
import requests
import re
import csv
import html

# A regex to match urls
# See https://urlregex.com/
URL_REGEX = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


# this is for the csv format from https://pretendyoure.xyz/zy/metrics/deck/2KK95 (Use "Download this deck as a CSV file")
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

        data = r.content.decode('utf-8')
        cr = csv.reader(data.splitlines(), delimiter=',')
        cards = list(cr)
        head = cards[0]
        cards = cards[1::]

        # Check if the data is valid
        if (("color" not in head) or ("text" not in head) or ("pick" not in head)):
            raise CommandError("The csv data is invalid.")

        # Create the deck
        deck = Deck.objects.create(name=options["name"], official=options["official"])

        # Create the cards
        # NOTE: We can't use bulk create because we need to call the save() method
        for card in cards:
            text = ""
            for other_text in card[1::]:
                if len(other_text) > 1:
                    text += other_text
            text = html.unescape(text)
            if card[0] == "black":
                BlackCard.objects.create(deck=deck, text=text)
            elif card[0] == "white":
                WhiteCard.objects.create(deck=deck, text=text)
        
        self.stdout.write(self.style.SUCCESS("Successfully created the {official}deck '{deck_name}' with "
                                             "{black_card_count} black cards and {white_card_count} "
                                             "white cards!".format(official="official " if options["official"] else "",
                                                                   deck_name=deck.name,
                                                                   black_card_count=deck.blackcard_set.count(),
                                                                   white_card_count=deck.whitecard_set.count())))
