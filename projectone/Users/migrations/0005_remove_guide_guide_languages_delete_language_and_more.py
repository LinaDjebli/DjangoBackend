# Generated by Django 5.0.6 on 2024-07-07 16:05

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_language_remove_guide_guide_languages_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='guide_languages',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.AddField(
            model_name='guide',
            name='guide_languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German'), ('zh', 'Chinese'), ('ja', 'Japanese'), ('ar', 'Arabic'), ('ru', 'Russian'), ('pt', 'Portuguese'), ('it', 'Italian'), ('ko', 'Korean'), ('nl', 'Dutch'), ('sv', 'Swedish'), ('tr', 'Turkish'), ('pl', 'Polish'), ('vi', 'Vietnamese'), ('el', 'Greek'), ('th', 'Thai')], default='en', max_length=53),
            preserve_default=False,
        ),
    ]