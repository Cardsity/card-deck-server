from django.test import TestCase
from decks.forms import DeckAddForm
import json


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
