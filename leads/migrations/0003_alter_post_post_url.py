# Generated by Django 5.2.3 on 2025-06-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_post_post_trigger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_url',
            field=models.URLField(),
        ),
    ]
