# Generated by Django 5.1.6 on 2025-02-23 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_remove_exchange_requester_alter_exchange_puzzle'),
        ('puzzle', '0002_rename_published_puzzle_is_published_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchange',
            name='puzzle',
        ),
        migrations.AddField(
            model_name='exchange',
            name='puzzle_asked',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exchanges_asked', to='puzzle.puzzle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exchange',
            name='puzzle_proposed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='puzzle.puzzle'),
        ),
    ]
