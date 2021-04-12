from rest_framework import viewsets
from rest_framework import views
from main.serializers import SurveySerializer, SurveyFieldSerializer, SurveyFieldChoiceSerializer, \
    AnswerSerializer, AnswerFieldSerializer, UserSerializer
from main.models import Survey, SurveyField, SurveyFieldChoice, Answer, AnswerField
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from django.contrib.auth import get_user_model
from django.db.models import Q


class OwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action not in ['list', 'retrieve']:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]


class SurveyFieldViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyFieldSerializer
    queryset = SurveyField.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action not in ['list', 'retrieve']:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]


class SurveyFieldChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyFieldChoiceSerializer
    queryset = SurveyFieldChoice.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action not in ['list', 'retrieve']:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        return Response({'Success': True, 'data': '{}'.format(request.user)})


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    search_fields = ['=user']

    def get_queryset(self):
        user = self.request.user
        query = Q(user=user) | Q(anon=False) if user.id else Q(anon=False)
        query_user = self.request.query_params.get('user_id')
        if query_user:
            query = query & Q(user=query_user)
        return Answer.objects.filter(query)

    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            self.permission_classes = (OwnerPermission, IsAuthenticated)
        else:
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()


class AnswerFieldViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerFieldSerializer
    queryset = AnswerField.objects.all()


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
