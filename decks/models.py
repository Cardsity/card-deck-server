from django.db import models
import re

# The regex to match blanks in black cards
BLACK_CARD_BLANK_REGEX = re.compile(r"(____+)+")


class Deck(models.Model):
    """A deck."""
    name = models.CharField("Name", max_length=100)
    official = models.BooleanField("Official", default=False)

    def as_dict(self):
        """Returns a deck as a dict."""
        base_dict = {
            "id": self.pk,
            "name": self.name
        }

        # Add black cards
        black_cards = []
        for card in self.blackcard_set.all():
            black_cards.append(card.as_dict())
        base_dict["black_cards"] = black_cards
        # Add white cards
        white_cards = []
        for card in self.whitecard_set.all():
            white_cards.append(card.as_dict())
        base_dict["white_cards"] = white_cards

        return base_dict

    class Meta:
        # Order by desc primary key
        ordering = ["-official", "-pk"]


class BlackCard(models.Model):
    """A black card which belongs to a deck."""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    text = models.TextField("Text")
    blanks = models.PositiveIntegerField("Blank count")

    def as_dict(self):
        """Returns a black card as a dict."""
        return {
            "text": self.text,
            "blanks": self.blanks
        }

    def save(self, *args, **kwargs):
        self.blanks = len(BLACK_CARD_BLANK_REGEX.findall(self.text))
        super(BlackCard, self).save(*args, **kwargs)


class WhiteCard(models.Model):
    """A white card which belongs to a deck."""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    text = models.TextField("Text")

    def as_dict(self):
        """Returns a white card as a dict."""
        return {
            "text": self.text
        }
