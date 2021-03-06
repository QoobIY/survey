# Generated by Django 2.2.10 on 2021-04-11 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Survey')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Answer')),
            ],
        ),
        migrations.AlterField(
            model_name='surveyfield',
            name='field_type',
            field=models.CharField(choices=[('TEXT', 'text'), ('SINGLE', 'single'), ('MULTIPLE', 'multiple')], max_length=10),
        ),
        migrations.AlterField(
            model_name='surveyfield',
            name='survey_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='main.Survey'),
        ),
        migrations.AlterField(
            model_name='surveyfieldchoice',
            name='field_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choises', to='main.SurveyField'),
        ),
        migrations.CreateModel(
            name='AnswerTextField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('answer_field_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.AnswerField')),
            ],
        ),
        migrations.AddField(
            model_name='answerfield',
            name='survey_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.SurveyField'),
        ),
        migrations.AddField(
            model_name='answerfield',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.SurveyFieldChoice'),
        ),
    ]
