from django.db import models
import re

# The regex to match blanks in black cards
BLACK_CARD_BLANK_REGEX = re.compile(r"(____+)+")


class Deck(models.Model):
    """A deck."""
    name = models.CharField("Name", max_length=100)

    class Meta:
        # Order by desc primary key
        ordering = ["-pk"]


class BlackCard(models.Model):
    """A black card which belongs to a deck."""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    text = models.TextField("Text")
    blanks = models.PositiveIntegerField("Blank count")

    def save(self, *args, **kwargs):
        self.blanks = len(BLACK_CARD_BLANK_REGEX.findall(self.text))
        super(BlackCard, self).save(*args, **kwargs)


class WhiteCard(models.Model):
    """A white card which belongs to a deck."""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    text = models.TextField("Text")
