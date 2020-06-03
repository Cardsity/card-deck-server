from django.test import TestCase
from news.models import News, NewsTypes


class NewsModelTestCase(TestCase):
    """Tests the News model."""
    def setUp(self) -> None:
        # Create the two news objects
        news1 = News.objects.create(title="First", type=NewsTypes.Updates.CHANGELOG, content="Hello :)")
        news2 = News.objects.create(title="Second", type=NewsTypes.Server.MAINTENANCE, content="Another hello '-'")

        # Get the time when the objects were created
        self.first_time = news1.created_at
        self.second_time = news2.created_at

    def test_as_dict(self):
        """Tests if the as_dict() method of the News model returns the correct result."""
        # Get the news
        news1 = News.objects.get(title="First")
        news2 = News.objects.get(title="Second")

        # Compare the dict of the first news
        self.assertDictEqual(news1.as_dict(), {
            "id": 1,
            "title": "First",
            "type": "UC",
            "content": "Hello :)",
            "created_at": self.first_time
        }, "The dict returned by as_dict() for the first news doesn't match the expected result!")

        # Compare the dict of the second news
        self.assertDictEqual(news2.as_dict(), {
            "id": 2,
            "title": "Second",
            "type": "SM",
            "content": "Another hello '-'",
            "created_at": self.second_time
        }, "The dict returned by as_dict() for the second news doesn't match the expected result!")

    def test_get_all_news_as_dict(self):
        """Tests if the all_news_as_dict() method of the News model returns the correct result."""
        # Get a dict containing all news
        all_news = News.get_all_news_as_dict()

        # Check the returned list
        self.assertDictEqual(all_news, {
            "news": [
                {
                    "id": 2,
                    "title": "Second",
                    "type": "SM",
                    "content": "Another hello '-'",
                    "created_at": self.second_time
                },
                {
                    "id": 1,
                    "title": "First",
                    "type": "UC",
                    "content": "Hello :)",
                    "created_at": self.first_time
                }
            ]
        }, "The list returned by get_all_news_as_dict() doesn't return the expected result!")
