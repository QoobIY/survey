from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Survey(models.Model):
    """Атрибуты опроса: название, дата старта, дата окончания, описание"""
    name = models.CharField(max_length=150, null=False)
    start_date = models.DateField(null=False, auto_now_add=True)
    end_date = models.DateField(null=False)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return "Survey<id={}, {}: {} - {}>".format(self.id, self.name, self.start_date, self.end_date)


# тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)
SURVEY_FIELDS = [
    ('TEXT', 'text'),
    ('SINGLE', 'single'),
    ('MULTIPLE', 'multiple'),
]


class SurveyField(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='fields')
    field_type = models.CharField(max_length=10, null=False, choices=SURVEY_FIELDS)
    question = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return "SurveyField<id={}, survey={}, field_type={}, question={}>".format(self.id, self.survey, self.field_type, self.question)

    def short_str(self) -> str:
        return "SurveyField<id={}, field_type={}>".format(self.id, self.field_type)


class SurveyFieldChoice(models.Model):
    field = models.ForeignKey(SurveyField, on_delete=models.CASCADE, related_name='choises')
    value = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return "SurveyFieldChoice<id={}, field_id={}, value={}>".format(self.id, self.field.id, self.value)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    anon = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Answer<id={}, user={}, survey={}>".format(self.id, self.user, self.survey)


class AnswerField(models.Model):
    """
        Если тип поля SINGLE или MULTIPLE, то в value помещаем id SurveyFieldChoice,
        иначе находим SurveyAnswerTextField с id текущего SurveyAnswerField
    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='fields')
    survey_field = models.ForeignKey(SurveyField, on_delete=models.CASCADE)
    value = models.ForeignKey(SurveyFieldChoice, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return "AnswerField<id={}, survey_field={}>".format(self.id, self.survey_field.short_str())


class AnswerTextField(models.Model):
    answer_field = models.OneToOneField(AnswerField, on_delete=models.CASCADE, related_name='text_field')
    value = models.TextField()
