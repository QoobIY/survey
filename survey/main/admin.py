from django.contrib import admin
from main.models import Survey, SurveyField, SurveyFieldChoice
# Register your models here.

admin.register(Survey)
admin.register(SurveyField)
admin.register(SurveyFieldChoice)
