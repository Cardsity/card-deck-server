# Generated by Django 3.0.6 on 2020-06-03 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-created_at'], 'verbose_name': 'news', 'verbose_name_plural': 'news'},
        ),
    ]
