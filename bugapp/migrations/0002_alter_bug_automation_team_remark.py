# Generated by Django 5.0.4 on 2024-04-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='automation_team_remark',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
