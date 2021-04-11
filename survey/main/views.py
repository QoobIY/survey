from rest_framework import viewsets
from main.serializers import SurveySerializer, SurveyFieldSerializer, SurveyFieldChoiceSerializer, \
    AnswerSerializer, AnswerFieldSerializer, AnswerTextFieldSerializer, AnswerFieldCreateSerializer,  \
    UserSerializer
from main.models import Survey, SurveyField, SurveyFieldChoice, Answer, AnswerField, AnswerTextField
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import get_user_model


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]


class SurveyFieldViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyFieldSerializer
    queryset = SurveyField.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]


class SurveyFieldChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyFieldChoiceSerializer
    queryset = SurveyFieldChoice.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        return Response({'Success': True, 'data': '{}'.format(request.user)})


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerFieldViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerFieldSerializer
    queryset = AnswerField.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerFieldCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AnswerTextFieldViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerTextFieldSerializer
    queryset = AnswerTextField.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    """https://stackoverflow.com/a/29391122"""
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        if self.action == 'list':
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()
