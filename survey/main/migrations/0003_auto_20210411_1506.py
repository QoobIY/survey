# Generated by Django 2.2.10 on 2021-04-11 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210411_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerfield',
            name='answer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='main.Answer'),
        ),
    ]