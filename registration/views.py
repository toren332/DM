from rest_framework.views import APIView
from . import models
from django.http import JsonResponse
from registration import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ML.filterandsort import filter_and_sort
from rest_framework.permissions import IsAuthenticated


class Profiles(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()


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
        serializer = serializers.PhoneCodeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"send": True}, status=201)
        return JsonResponse({"send": False}, status=400)


class CheckSmsCode(APIView):
    def post(self, request, format=None):
        phone = request.data['phone']
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
        data = request.data

        serializer = serializers.FilterAndSortSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile = models.Profile.objects.get(user=request.user)
        error, queryset = filter_and_sort(data, self.get_queryset(), profile=profile)
        if error['ERROR'] is not None:
            return Response(error, status=status.HTTP_409_CONFLICT)
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

        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = serializers.ShoesShortSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
