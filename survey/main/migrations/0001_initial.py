# Generated by Django 2.2.10 on 2021-04-10 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_type', models.CharField(choices=[('TEXT', 'text'), ('SINGLE', 'single'), ('MULTIPLE', 'multiple')], max_length=8)),
                ('question', models.CharField(max_length=255)),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyFieldChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('field_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.SurveyField')),
            ],
        ),
    ]
