# Generated by Django 5.2.3 on 2025-06-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_trigger',
            field=models.CharField(blank=True, choices=[('task', 'Task'), ('offer', 'Offer')], max_length=20, null=True),
        ),
    ]
