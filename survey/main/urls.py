from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import path, include
from rest_framework import routers
from main import views
from rest_framework.authtoken import views as authtoken_views


class Test(APIView):

    def get(self, request):
        print(request.user)
        print(request.user.id)
        return Response({'Success': True, 'data': 'Hello'})


router = routers.DefaultRouter()


router.register(r'surveys', views.SurveyViewSet)
router.register(r'surveys_field', views.SurveyFieldViewSet)
router.register(r'surveys_field_choise', views.SurveyFieldChoiceViewSet)
router.register(r'answer', views.AnswerViewSet)
router.register(r'answer_field', views.AnswerFieldViewSet)
router.register(r'answer_text_field', views.AnswerTextFieldViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test', Test.as_view(), name='test'),
    path('profile', views.ProfileView.as_view()),
    path('api-token-auth/', authtoken_views.obtain_auth_token)
]
