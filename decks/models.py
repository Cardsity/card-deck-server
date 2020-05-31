from django.db import models


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


class WhiteCard(models.Model):
    """A white card which belongs to a deck."""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    text = models.TextField("Text")
