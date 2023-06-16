"""nope URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from nope.accounts import views as account_views
from nope.demo import views as demo_views
from . import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Nope API",
        default_version='0.1.0',
        description="Nope",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="copyright"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter(trailing_slash=False)
router.register('users', account_views.UserViewSet)

router.register('teacher', demo_views.SingleTeacherViewSet)
router.register('teacherStudents', demo_views.TeacherWithStudentViewSet)
router.register('student', demo_views.SingleStudentViewSet)
router.register('studentTeachers', demo_views.StudentWithTeacherViewSet)

urlpatterns = [
                  path('api/', include(router.urls)),
                  path('api/profile', account_views.ProfileAPIView.as_view()),
                  path('api/auth/login', account_views.LoginAPIView.as_view()),
                  path('api/auth/logout', account_views.LogoutAPIView.as_view()),
                  path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/auth/send-sms', account_views.SendSMSCodeAPIView.as_view()),

                  path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
