# Generated by Django 4.0.2 on 2023-11-07 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createcourse', '0003_rename_key_publicquestions_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
