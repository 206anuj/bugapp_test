# Generated by Django 5.0.4 on 2024-04-24 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugapp', '0004_bug_issue_closer_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='automation_team_update',
            field=models.BooleanField(),
        ),
    ]