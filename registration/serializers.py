from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
import random
from registration.smsc_api import *


def send_sms(phone, text):
    smsc = SMSC()
    smsc.send_sms(str(phone), str(text), sender='DRESS-ME')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.IntegerField(min_value=70000000000, max_value=79999999999, required=True)
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        valid_username = User.objects.filter(username=validated_data['username'])
        if valid_username:
            raise serializers.ValidationError("This user already exist")
        else:
            user = User.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password'])
        return user

    def update(self, instance: models.User, validated_data):
        for (key, value) in validated_data.items():
            if key == 'username':

                users_by_username = User.objects.filter(username=validated_data['username'])
                if users_by_username:
                    user_by_username = users_by_username[0]
                    if user_by_username.username != instance.username:
                        raise serializers.ValidationError("This phone already used")
                    else:
                        setattr(instance, key, value)
                        phone_code = models.PhoneCode.objects.get(phone=value)
                        phone_code.delete()
                else:
                    setattr(instance, key, value)
                    phone_code = models.PhoneCode.objects.get(phone=value)
                    phone_code.delete()

            if key == 'password':
                instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'password', 'username')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = models.Profile
        fields = ('user', 'name', 'email', 'gender', 'shoes_size')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        phone_code0 = models.PhoneCode.objects.filter(phone=user_data['username'])
        if phone_code0:  # Если существует этот телефон в проверочной базе
            phone_code = models.PhoneCode.objects.get(phone=user_data['username'])
            if phone_code.is_verified:  # Если телефон верифицирован в проверочной базе
                user = UserSerializer.create(UserSerializer(), validated_data=user_data)
                profile_one = models.Profile.objects.create(user=user)

                for (key, value) in validated_data.items():
                    setattr(profile_one, key, value)
                profile_one.save()
                phone_code.delete()
                return profile_one

        raise serializers.ValidationError("This phone is not verified")

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            if key == 'user':
                user_data = validated_data.get('user')
                if user_data.get('username'):
                    phone_code0 = models.PhoneCode.objects.filter(phone=user_data['username'])
                    if phone_code0:  # Если существует этот телефон в проверочной базе
                        phone_code = models.PhoneCode.objects.get(phone=user_data['username'])
                        if phone_code.is_verified:  # Если телефон верифицирован в проверочной базе
                            instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
                        else:
                            raise serializers.ValidationError("This phone is not verified")
                    else:
                        raise serializers.ValidationError("This phone is not verified")
                else:
                    instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance


class PhoneCodeSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(min_value=70000000000, max_value=79999999999, required=True)
    code = serializers.IntegerField(min_value=0, max_value=9999, required=False)
    is_verified = serializers.BooleanField(required=False)

    def create(self, validated_data):
        valid_phone = models.PhoneCode.objects.filter(phone=validated_data['phone'])
        if valid_phone:
            phone_code = models.PhoneCode.objects.get(phone=validated_data['phone'])
            phone_code.code = random.randint(1000, 9999)
            phone_code.save()
            send_sms(phone=validated_data['phone'], text=phone_code.code)
        else:
            code = random.randint(1000, 9999)
            phone_code = models.PhoneCode.objects.create(phone=validated_data['phone'], code=code)
            phone_code.save()
            send_sms(phone=validated_data['phone'], text=phone_code.code)
        return phone_code

    class Meta:
        model = models.PhoneCode
        fields = ('phone', 'code', 'is_verified')


class ShoesSerializer(serializers.ModelSerializer):
    about = serializers.ReadOnlyField()

    class Meta:
        model = models.ShoesItem
        exclude = ('top_material', 'inside_material', 'bottom_material', 'step_material', 'height',
                   'country', 'season', 'color', 'zip_type', 'furniture_color', 'sport_type')


class ShoesShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShoesItem
        fields = ('id', 'image_main', 'name', 'subsubcategory', 'subcategory', 'category', 'price', 'brand')


class FilterSerializer(serializers.Serializer):

    class PriceFilterSerializer(serializers.Serializer):
        start_price = serializers.IntegerField()
        end_price = serializers.IntegerField()

    class BrandFilterSerializer(serializers.Serializer):
        brand = serializers.ListField(
            child=serializers.CharField()
        )

    class ColorFilterSerializer(serializers.Serializer):
        color_CHOICES = models.ShoesItem.color_CHOICES
        color = serializers.ListField(
            child=serializers.ChoiceField(color_CHOICES)
        )

    class SubategoryFilterSerializer(serializers.Serializer):
        subcategory_CHOICES = models.ShoesItem.subcategory_CHOICES
        subcategory = serializers.ListField(
            child=serializers.ChoiceField(subcategory_CHOICES)
        )

    class SeasonFilterSerializer(serializers.Serializer):
        season_CHOICES = models.ShoesItem.season_CHOICES
        subcategory = serializers.ListField(
            child=serializers.ChoiceField(season_CHOICES)
        )

    price_filter = PriceFilterSerializer(required=False)
    brand_filter = BrandFilterSerializer(required=False)
    color_filter = ColorFilterSerializer(required=False)
    category_filter = SubategoryFilterSerializer(required=False)
    season_filter = SeasonFilterSerializer(required=False)


class SortSerializer(serializers.Serializer):
    price_CHOICES = (
        ('to_cheap', 'TO_CHEAP'),
        ('from_cheap', 'FROM_CHEAP')
    )
    price_sort = serializers.ChoiceField(choices=price_CHOICES, required=False)


class FilterAndSortSerializer(serializers.Serializer):
    filter = FilterSerializer(required=False)
    sort = SortSerializer(required=False)


class RatingSerializer(serializers.Serializer):
    likes = serializers.BooleanField(required=False)
    dislikes = serializers.BooleanField(required=False)
    bought = serializers.BooleanField(required=False)
    saw = serializers.BooleanField(required=False)
    favourite = serializers.BooleanField(required=False)
