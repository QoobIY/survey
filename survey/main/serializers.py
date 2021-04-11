from rest_framework import serializers
from main.models import Survey, SurveyField, SurveyFieldChoice, Answer, AnswerField, AnswerTextField
from django.contrib.auth import get_user_model


class SurveyFieldChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFieldChoice
        fields = '__all__'


class SurveyFieldSerializer(serializers.ModelSerializer):
    choises = SurveyFieldChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyField
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    fields = SurveyFieldSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'


class AnswerTextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTextField
        fields = '__all__'

    def validate(self, data):
        if data['value']:
            pass
        return data


class AnswerFieldSerializer(serializers.ModelSerializer):
    text_field = AnswerTextFieldSerializer(read_only=True)
    survey_field = SurveyFieldSerializer()

    class Meta:
        model = AnswerField
        fields = '__all__'


class AnswerFieldCreateSerializer(serializers.ModelSerializer):
    text_field = AnswerTextFieldSerializer(read_only=True)

    class Meta:
        model = AnswerField
        fields = '__all__'

    def validate(self, data):
        print('validate', data)
        print('fields', data['answer'].survey.fields)
        print('survey_ in in survey_field', )
        print('survey_ in in ans', data['answer'].survey.id)
        if data['survey_field'].survey.id != data['answer_'].survey.id:
            raise serializers.ValidationError({
                'survey_field': 'Survey field does not belong to this answer {}'.format(data['answer'])
                })
        if data['value'] and data['value'].field != data['survey_field']:
            raise serializers.ValidationError({
                'value': 'Value does not belong to survey field {}'.format(data['survey_field'])
                })
        return data


class AnswerSerializer(serializers.ModelSerializer):
    fields = AnswerFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """https://stackoverflow.com/a/29391122"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email',)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)
