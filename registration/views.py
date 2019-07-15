from rest_framework.views import APIView
from . import models
from django.http import JsonResponse
from registration import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ML.filterandsort import filter_and_sort
from rest_framework.permissions import IsAuthenticated
import random
from ML.create_table import create_random_table
from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Profiles(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()

    @action(detail=False, methods=['GET', 'PATCH',])
    def me(self, request):
        if request.method != 'GET':
            data = request.data
            user = request.user
            profile = models.Profile.objects.get(user=user)
            serializer = serializers.ProfileSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.update(instance=profile, validated_data=data)
            serializer = serializers.ProfileSerializer(instance=profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = request.user
            profile = models.Profile.objects.get(user=user)
            serializer = serializers.ProfileSerializer(instance=profile)
            return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordCustomAuthToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get("phone")
        password = request.data.get("password")
        if username is None or password is None:
            return JsonResponse({"login": False, "error": "need phone and password fields"})
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({"login": False})
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})


class AuthSms(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get("phone")
        code = request.data.get("code")

        if username is None:
            return JsonResponse({"login": False, "error": "need phone field"})

        if code is None:
            return JsonResponse({"login": False, "error": "need code field"})

        if not models.User.objects.filter(username=username):
            valid_phone = models.PhoneCode.objects.filter(phone=username)
            if valid_phone:
                phone_code = models.PhoneCode.objects.get(phone=username)
                if phone_code.code == code:
                    phone_code.delete()
                    user = serializers.UserSerializer.create(serializers.UserSerializer(), validated_data={"username": username})
                    models.Profile.objects.create(user=user)
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({"token": token.key}, status=200)
                else:
                    return JsonResponse({"login": False, "error": "wrong code"}, status=400)

            else:
                return JsonResponse({"login": False, "error": "sms not sanded"}, status=400)
        else:
            valid_phone = models.PhoneCode.objects.filter(phone=username)
            if valid_phone:
                phone_code = models.PhoneCode.objects.get(phone=username)
                if phone_code.code == code:
                    phone_code.delete()
                    user = models.User.objects.get(username=username)
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'token': token.key})
                else:
                    return JsonResponse({"login": False, "error": "wrong code"}, status=400)

            else:
                return JsonResponse({"login": False, "error": "sms not sanded"}, status=400)


class SendSmsCode(APIView):
    def post(self, request, format=None):
        serializer = serializers.PhoneCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return JsonResponse({"send": True}, status=201)


class CheckSmsCode(APIView):
    def post(self, request, format=None):
        if request.data.get('phone'):
            phone = request.data['phone']
        else:
            return JsonResponse({"login": False, "error": "need phone field"})

        if request.data.get('code'):
            code = request.data['code']
        else:
            return JsonResponse({"checked": False, 'error': 'Need code'}, status=400)
        valid_phone = models.PhoneCode.objects.filter(phone=phone)
        if valid_phone:
            phone_code = models.PhoneCode.objects.get(phone=phone)
            if phone_code.code == code:
                phone_code.is_verified = True
                phone_code.save()
                return JsonResponse({"checked": True}, status=200)
        return JsonResponse({"checked": False}, status=400)


class Shoes(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ShoesSerializer
    queryset = models.ShoesItem.objects.all()

    @action(detail=False, methods=['POST'])
    def ml(self, request):
        PAGE_ITEMS_SIZE = 32
        page = request.GET.get('page')
        data = request.data

        serializer = serializers.FilterAndSortSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile = models.Profile.objects.get(user=request.user)
        error, queryset = filter_and_sort(data, self.get_queryset(), profile=profile)
        if error['ERROR'] is not None:
            return Response(error, status=status.HTTP_409_CONFLICT)
        if page:
            page = int(page)
            queryset = queryset[(page - 1) * PAGE_ITEMS_SIZE:page * PAGE_ITEMS_SIZE]
        serializer = serializers.ShoesShortSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk=None):
        data = request.data
        serializer = serializers.RatingSerializer(data=data)
        profile = models.Profile.objects.get(user=request.user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if data.get('likes'):
            if data['likes']==True:
                profile.likes.add(models.ShoesItem.objects.get(id=pk))
            else:
                profile.likes.remove(models.ShoesItem.objects.get(id=pk))
        if data.get('dislikes'):
            if data['dislikes']==True:
                profile.dislikes.add(models.ShoesItem.objects.get(id=pk))
            else:
                profile.dislikes.remove(models.ShoesItem.objects.get(id=pk))
        if data.get('saw'):
            if data['saw']==True:
                profile.saw.add(models.ShoesItem.objects.get(id=pk))
            else:
                profile.saw.remove(models.ShoesItem.objects.get(id=pk))
        if data.get('bought'):
            if data['bought']==True:
                profile.bought.add(models.ShoesItem.objects.get(id=pk))
            else:
                profile.bought.remove(models.ShoesItem.objects.get(id=pk))
        if data.get('favourite'):
            if data['favourite']==True:
                profile.favourite.add(models.ShoesItem.objects.get(id=pk))
            else:
                profile.favourite.remove(models.ShoesItem.objects.get(id=pk))

        return Response('', status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def brands(self, request):
        brand_lists = list(models.ShoesItem.objects.values_list('brand'))
        brandlist = []
        for i in brand_lists:
            brandlist.append(i[0])

        return Response(list(set(brandlist)), status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ShoesShortSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class Random_table(APIView):
    def post(self, request, format=None):
        if request.data.get('start'):
            start = request.data['start']
            if start:
                create_random_table()
                return JsonResponse({"created": True}, status=201)
        return JsonResponse({"created": False}, status=400)



