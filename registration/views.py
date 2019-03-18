from rest_framework.views import APIView
from .models import Profile, PhoneCode
from django.http import JsonResponse
from registration.serializers import ProfileSerializer, PhoneCodeSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins


class Profiles(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class CustomAuthToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return JsonResponse({"login": False})
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({"login": False})
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})


class SendSmsCode(APIView):
    def post(self, request, format=None):
        serializer = PhoneCodeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"send":True}, status=201)
        return JsonResponse({"send":False}, status=400)

class CheckSmsCode(APIView):
    def post(self, request, format=None):
        phone=request.data['phone']
        if request.data.get('code'):
            code = request.data['code']
        else:
            return JsonResponse({"checked": False, 'error':'Need code'}, status=400)
        valid_phone=PhoneCode.objects.filter(phone=phone)
        if valid_phone:
            phone_code=PhoneCode.objects.get(phone=phone)
            if phone_code.code == code:
                phone_code.is_verified=True
                phone_code.save()
                return JsonResponse({"checked":True}, status=200)
        return JsonResponse({"checked":False}, status=400)
