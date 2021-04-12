from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from main.models import Survey, SurveyField, SurveyFieldChoice, Answer, AnswerField, AnswerTextField
from django.contrib.auth import get_user_model


class SurveyFieldChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFieldChoice
        fields = '__all__'

    def validate_field(self, data):
        if data.field_type == 'TEXT':
            raise serializers.ValidationError('Choice is available only for fields of type MULTIPLE/SINGLE')
        return data


class SurveyFieldSerializer(serializers.ModelSerializer):
    choises = SurveyFieldChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyField
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    fields = SurveyFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'


class AnswerTextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTextField
        fields = ['value']

    def validate(self, data):
        if data['value']:
            pass
        return data


class AnswerFieldSerializer(serializers.ModelSerializer):
    text_field = AnswerTextFieldSerializer(required=False)

    class Meta:
        model = AnswerField
        fields = ['survey_field', 'value', 'text_field']

    def validate(self, data):
        # if data['survey_field'].survey.id != data['answer'].survey.id:
        #     raise serializers.ValidationError({
        #         'survey_field': 'Survey field does not belong to this answer {}'.format(data['answer'])
        #         })
        if data['survey_field'].field_type != 'TEXT' and 'value' not in data:
            raise serializers.ValidationError({
                    'survey_field': 'Choose at least 1 value for {}'.format(data['survey_field'])
                    })
        if 'value' in data:
            if data['survey_field'].field_type == 'TEXT':
                raise serializers.ValidationError({'value': 'Value not allowed for TEXT field_type in {}'.format(data['survey_field'])})
            if data['value'].field != data['survey_field']:
                raise serializers.ValidationError({
                    'value': 'Value does not belong to survey field {}'.format(data['survey_field'])
                    })
        if data['survey_field'].field_type == 'TEXT' and 'text_field' not in data:
            raise serializers.ValidationError({'text_field': 'text_field required for {}'.format(data['survey_field'])})
        elif data['survey_field'].field_type != 'TEXT' and 'text_field' in data:
            raise serializers.ValidationError({'text_field': 'text_field not allowed for {}'.format(data['survey_field'])})
        return data


class AnswerSerializer(serializers.ModelSerializer):
    fields = AnswerFieldSerializer(many=True)
    # user = serializers.RelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        answer = Answer.objects.filter(user=user, survey=attrs['survey'])
        print('answer validate', attrs)
        for field in attrs['fields']:
            if field['survey_field'].survey != attrs['survey']:
                raise serializers.ValidationError({'fields': '{} does not belong to survey {}'
                                                   .format(field['survey_field'], attrs['survey'])})
        attrs['user'] = user
        if answer.exists():
            raise serializers.ValidationError({'survey': 'You have already completed this survey'})
        return super().validate(attrs)

    def create(self, validated_data):
        print('validated data', validated_data)
        fields = validated_data.pop('fields')
        answer = Answer.objects.create(**validated_data)
        for field in fields:
            text_field = field.pop('text_field') if 'text_field' in field else None
            answer_field = AnswerField.objects.create(answer=answer, **field)
            if text_field:
                print('text field in!', text_field)
                AnswerTextField.objects.create(**text_field, answer_field=answer_field)
        return answer


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
