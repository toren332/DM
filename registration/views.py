from rest_framework.views import APIView
from .models import Profile
from django.http import JsonResponse
from registration.serializers import ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

class ProfileList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {"detail": "You are not authorize"}
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        if request.user.is_authenticated:
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, format=None):
        data = request.data
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ProfileDetail(APIView):
    def get(self, request, user_id, format=None):
        profile_one = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile_one)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, user_id, format=None):
        data = request.data
        profile_one = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile_one, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request, user_id, format=None):
        data = request.data
        current_user = request.user
        if current_user.id == user_id:
            profile_one = Profile.objects.get(user_id=user_id)
            serializer = ProfileSerializer(profile_one, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse({"PTCH":False,"ERROR":"try to change another user"}, status=400)

    def delete(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            user_one = User.objects.get(id=user_id)
            user_one.delete()
            data = {
                "user": "deleted"
            }
            return JsonResponse(data, safe=False)
        return JsonResponse({"DEL":False,"ERROR":"try to delete another user"}, status=400)


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



