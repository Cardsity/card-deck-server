from django import forms
import json


class DeckAddForm(forms.Form):
    """Form for adding a deck."""
    name = forms.CharField(label="Name", max_length=100)
    card_json = forms.CharField(widget=forms.HiddenInput)

    def clean_card_json(self):
        """
        Check if the supplied card json is valid. Additionally, the json will be parsed.
        TODO: Use dynamic field generation for this.
        """
        data = self.cleaned_data["card_json"]

        # Check if the data is valid json
        parsed_json = None
        try:
            parsed_json = json.loads(data)
        except ValueError:
            raise forms.ValidationError("Invalid json data.")

        # Check if the necessary keys are in the json object
        if ("black_cards" not in parsed_json) or ("white_cards" not in parsed_json):
            raise forms.ValidationError("Not all cards where supplied.")

        # Loop over black cards and "clean" them
        valid_entries = []
        for i in range(len(parsed_json["black_cards"])):
            value = parsed_json["black_cards"][i].strip()
            # Check if the trimmed value is not an empty string
            if value != "":
                # Check if the length is longer than 128 chars (max length for a card)
                if len(value) > 128:
                    raise forms.ValidationError("There is a black card with more than 128 characters!")
                valid_entries.append(value)
        parsed_json["black_cards"] = valid_entries
        # Loop over white cards and "clean" them
        valid_entries = []
        for i in range(len(parsed_json["white_cards"])):
            value = parsed_json["white_cards"][i].strip()
            # Check if the trimmed value is not an empty string
            if value != "":
                # Check if the length is longer than 128 chars (max length for a card)
                if len(value) > 128:
                    raise forms.ValidationError("There is a white card with more than 128 characters!")
                valid_entries.append(value)
        parsed_json["white_cards"] = valid_entries

        # Check the card amount
        # Max. 100 cards, min. 5 black cards & 5 white cards
        if len(parsed_json["black_cards"]) + len(parsed_json["white_cards"]) > 100:
            raise forms.ValidationError("A maximum of 100 cards are allowed.")
        if len(parsed_json["black_cards"]) < 5 or len(parsed_json["white_cards"]) < 5:
            raise forms.ValidationError("A minimum of 5 black cards and 5 white cards need to be present.")

        return parsed_json
