from django.db import models


class NewsTypes:
    """Holds a list of news types."""
    class Updates:
        """Game updates."""
        ADDED = "UA"
        FIXED = "UF"
        REMOVED = "UR"
        CHANGELOG = "UC"

    class Server:
        """News related to the server."""
        MAINTENANCE = "SM"


class News(models.Model):
    """Stores a news."""
    title = models.CharField("Title", max_length=100)
    type = models.CharField("Type", max_length=2, choices=[
        ('Updates', (
            (NewsTypes.Updates.ADDED, "Added"),
            (NewsTypes.Updates.FIXED, "Fixed"),
            (NewsTypes.Updates.REMOVED, "Removed"),
            (NewsTypes.Updates.CHANGELOG, "Changelog"),
        )),
        ('Server', (
            (NewsTypes.Server.MAINTENANCE, "Maintenance"),
        ))
    ])
    content = models.TextField("Content")
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def as_dict(self):
        """Returns a news as a dict."""
        return {
            "id": self.pk,
            "title": self.title,
            "type": self.type,
            "content": self.content,
            "created_at": self.created_at
        }

    @classmethod
    def get_all_news_as_dict(cls):
        """Returns all news as a list. Every news is a dict (see as_dict() method)."""
        # Generate a list with all dicts of the news
        news_list = []
        for n in News.objects.all():
            news_list.append(n.as_dict())

        # Return the list
        return news_list

    class Meta:
        # Order by date desc
        ordering = ['-created_at']
