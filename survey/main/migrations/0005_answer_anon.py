# Generated by Django 2.2.10 on 2021-04-12 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210411_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='anon',
            field=models.BooleanField(default=False),
        ),
    ]
