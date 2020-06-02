from django.db import migrations


def forwards(apps, schema_editor):
    """Sets the blank count of every field to 1 where the value is 0."""
    BlackCard = apps.get_model("decks", "BlackCard")
    for row in BlackCard.objects.all():
        if row.blanks == 0:
            row.blanks = 1  # Technically, we don't need this line since the save method should do everything for us
            row.save()


class Migration(migrations.Migration):
    dependencies = [
        ('decks', '0004_auto_20200601_1221'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
