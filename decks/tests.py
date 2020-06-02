from django.test import TestCase
from decks.forms import DeckAddForm
import json
from decks.models import Deck, BlackCard, WhiteCard


class DeckAddFormTestCase(TestCase):
    """Tests everything related to the DeckAddForm."""
    # TODO: Make method for creating DeckAddForm
    def setUp(self) -> None:
        """Sets some values which can come in handy for the tests."""
        # Every name with this length until the specified one will be tested
        self.max_name_length = 100
        # Valid name
        self.valid_name_min_length = 'a'

        # Set some values for the test
        self.min_black_cards = 5
        self.min_white_cards = 5
        self.max_card_length = 64
        self.max_card_amount = 100

        # Make valid cards
        # Minimum length
        self.valid_black_cards_min_amount = ['a' for i in range(self.min_black_cards)]
        self.valid_white_cards_min_amount = ['b' for i in range(self.min_white_cards)]
        self.valid_card_dict_min_amount = {
            "black_cards": self.valid_black_cards_min_amount,
            "white_cards": self.valid_white_cards_min_amount
        }
        self.valid_card_json_min_amount = json.dumps(self.valid_card_dict_min_amount)

    def test_name(self):
        """Tests the name attribute of the DeckAddForm."""
        # Test every name length until the specified max length
        # NOTE: This includes the attribute self.valid_name_min_length
        for i in range(1, self.max_name_length + 1):
            form = DeckAddForm(data={
                "name": 'a' * i,
                "card_json": self.valid_card_json_min_amount
            })
            self.assertTrue(form.is_valid())

        # Test the name with a length which is longer than the max length
        form = DeckAddForm(data={
            "name": 'a' * (self.max_name_length + 1),
            "card_json": self.valid_card_json_min_amount
        })
        self.assertFalse(form.is_valid())

    def test_card_json(self):
        """Tests the card_json attribute of the DeckAddForm."""
        # Check for invalid json
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": "invalid json xyz"
        })
        self.assertFalse(form.is_valid())

        # Check if parameters are not supplied
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": []
            })
        })
        self.assertFalse(form.is_valid())
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "white_cards": []
            })
        })
        self.assertFalse(form.is_valid())

        # Check the values under the minimum amount of black cards
        for i in range(1, self.min_black_cards):
            form = DeckAddForm(data={
                "name": self.valid_name_min_length,
                "card_json": json.dumps({
                    "black_cards": ['a' for j in range(i)],
                    "white_cards": self.valid_white_cards_min_amount
                })
            })
            self.assertFalse(form.is_valid())

        # Check the values under the minimum amount of white cards
        for i in range(1, self.min_white_cards):
            form = DeckAddForm(data={
                "name": self.valid_name_min_length,
                "card_json": json.dumps({
                    "black_cards": self.valid_black_cards_min_amount,
                    "white_cards": ['b' for j in range(i)]
                })
            })
            self.assertFalse(form.is_valid())

        # Check the minimum amount of cards
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": self.valid_black_cards_min_amount,
                "white_cards": self.valid_white_cards_min_amount
            })
        })
        self.assertTrue(form.is_valid())

        # Check the maximum amount of cards
        black_card_amount = 0
        white_card_amount = 0
        # Check if the maximum number is even
        if self.max_card_amount % 2 == 0:
            # Both should have the same amount of cards
            black_card_amount = white_card_amount = int(self.max_card_amount / 2)
        else:
            # There should be one more black card than white card
            black_card_amount = int((self.max_card_amount / 2) + 0.5)
            white_card_amount = int((self.max_card_amount / 2) - 0.5)
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": ['a' for i in range(black_card_amount)],
                "white_cards": ['b' for i in range(white_card_amount)]
            })
        })
        self.assertTrue(form.is_valid())

        # Check max amount of cards + 1
        white_card_amount += 1
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": ['a' for i in range(black_card_amount)],
                "white_cards": ['b' for i in range(white_card_amount)]
            })
        })
        self.assertFalse(form.is_valid())

        # Check the maximum card length on black cards
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": self.valid_black_cards_min_amount + ['a' * self.max_card_length],
                "white_cards": self.valid_white_cards_min_amount
            })
        })
        self.assertTrue(form.is_valid())
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": self.valid_black_cards_min_amount + ['a' * (self.max_card_length + 1)],
                "white_cards": self.valid_white_cards_min_amount
            })
        })
        self.assertFalse(form.is_valid())

        # Check the maximum card length on white cards
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": self.valid_black_cards_min_amount,
                "white_cards": self.valid_white_cards_min_amount + ['b' * self.max_card_length]
            })
        })
        self.assertTrue(form.is_valid())
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": json.dumps({
                "black_cards": self.valid_black_cards_min_amount,
                "white_cards": self.valid_white_cards_min_amount + ['b' * (self.max_card_length + 1)]
            })
        })
        self.assertFalse(form.is_valid())

    def test_parameters_are_needed(self):
        """Tests if all supplied parameters are needed in the DeckAddForm."""
        # Create the form with all missing parameters
        form = DeckAddForm()
        self.assertFalse(form.is_valid())

        # Create the form with missing name
        form = DeckAddForm(data={
            "card_json": self.valid_card_json_min_amount
        })
        self.assertFalse(form.is_valid())

        # Create the form with missing card_json
        form = DeckAddForm(data={
            "name": self.valid_name_min_length
        })
        self.assertFalse(form.is_valid())

        # Create the form with all data supplied
        form = DeckAddForm(data={
            "name": self.valid_name_min_length,
            "card_json": self.valid_card_json_min_amount
        })
        self.assertTrue(form.is_valid())


class DeckModelTestCase(TestCase):
    """Checks the models Deck, BlackCard and WhiteCard."""
    def setUp(self) -> None:
        # Create new decks
        deck2 = Deck.objects.create(name='Second', official=True)

        # Create new cards for deck2
        self.card1_text = "a ____"
        BlackCard.objects.create(deck=deck2, text=self.card1_text)
        self.card2_text = "________ b _____________________"
        BlackCard.objects.create(deck=deck2, text=self.card2_text)
        self.card3_text = "c ___"
        BlackCard.objects.create(deck=deck2, text=self.card3_text)
        self.card4_text = "d"
        BlackCard.objects.create(deck=deck2, text=self.card4_text)
        self.card5_text = "e"
        WhiteCard.objects.create(deck=deck2, text=self.card5_text)

    def test_black_card_blanks(self):
        """Checks if the blanks field of black cards is correct."""
        # Get the deck
        deck = Deck.objects.get(name='Second')

        # Check card 1
        card1 = BlackCard.objects.get(deck=deck, text=self.card1_text)
        self.assertEqual(card1.blanks, 1, "The blank count for card 1 is not correct!")

        # Check card 2
        card2 = BlackCard.objects.get(deck=deck, text=self.card2_text)
        self.assertEqual(card2.blanks, 2, "The blank count for card 2 is not correct!")

        # Check card 3
        card3 = BlackCard.objects.get(deck=deck, text=self.card3_text)
        self.assertEqual(card3.blanks, 1, "The blank count for card 3 is not correct!")

        # Check card 4
        card4 = BlackCard.objects.get(deck=deck, text=self.card4_text)
        self.assertEqual(card4.blanks, 1, "The blank count for card 4 is not correct!")

    def test_card_as_dict(self):
        """Tests if a card can be converted to a dict in the right way."""
        # Get the deck
        deck = Deck.objects.get(name='Second')

        # Check card 1
        card1 = BlackCard.objects.get(deck=deck, text=self.card1_text)
        card1_dict = card1.as_dict()
        self.assertDictEqual(card1_dict, {
            "text": self.card1_text,
            "blanks": 1
        }, "as_dict() doesn't give the correct result for card 1 (black card)!")

        # Check card 2
        card2 = BlackCard.objects.get(deck=deck, text=self.card2_text)
        card2_dict = card2.as_dict()
        self.assertDictEqual(card2_dict, {
            "text": self.card2_text,
            "blanks": 2
        }, "as_dict() doesn't give the correct result for card 2 (black card)!")

        # Check card 3
        card3 = BlackCard.objects.get(deck=deck, text=self.card3_text)
        card3_dict = card3.as_dict()
        self.assertDictEqual(card3_dict, {
            "text": self.card3_text,
            "blanks": 1
        }, "as_dict() doesn't give the correct result for card 3 (black card)!")

        # Check card 4
        card4 = BlackCard.objects.get(deck=deck, text=self.card4_text)
        card4_dict = card4.as_dict()
        self.assertDictEqual(card4_dict, {
            "text": self.card4_text,
            "blanks": 1
        }, "as_dict() doesn't give the correct result for card 4 (black card)!")

        # Check card 5
        card5 = WhiteCard.objects.get(deck=deck, text=self.card5_text)
        card5_dict = card5.as_dict()
        self.assertDictEqual(card5_dict, {
            "text": self.card5_text
        }, "as_dict() doesn't give the correct result for card 5 (white card)!")

    def test_deck_as_dict(self):
        """Tests if a deck can be converted to a dict in the right way."""
        # Get the deck
        deck = Deck.objects.get(name='Second')

        # Check if the dict is equal
        self.assertDictEqual(deck.as_dict(), {
            "id": 1,
            "name": "Second",
            "black_cards": [
                {
                    "text": self.card1_text,
                    "blanks": 1
                },
                {
                    "text": self.card2_text,
                    "blanks": 2
                },
                {
                    "text": self.card3_text,
                    "blanks": 1,
                },
                {
                    "text": self.card4_text,
                    "blanks": 1
                }
            ],
            "white_cards": [
                {
                    "text": self.card5_text
                }
            ]
        }, "as_dict() for the deck doesn't give the  result!")
