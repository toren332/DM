from django.contrib import admin
from django.urls import path
from registration import views
from registration.views import Profiles
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

router = DefaultRouter()
router.register('api/v0/profiles', Profiles, basename='profiles')
urlpatterns = router.urls
urlpatterns += [
    path('admin/', admin.site.urls),
    url(r'^api/v0/token-auth/', views.CustomAuthToken.as_view()),
    url(r'^api/v0/sms/send', views.SendSmsCode.as_view()),
    url(r'^api/v0/sms/check', views.CheckSmsCode.as_view()),

]

