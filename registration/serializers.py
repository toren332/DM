from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
import random
from django.contrib.auth.base_user import BaseUserManager
from registration.smsc_api import *


def send_sms(phone, text):
    smsc = SMSC()
    smsc.send_sms(str(phone), str(text), sender='DRESS-ME')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.IntegerField(min_value=70000000000, max_value=79999999999, required=False)
    password = serializers.CharField(min_length=8, required=False)

    def create(self, validated_data):
        valid_username = User.objects.filter(username=validated_data['username'])
        if valid_username:
            raise serializers.ValidationError("This user already exist")
        else:
            user = User.objects.create_user(username=validated_data['username'],
                                            password=BaseUserManager().make_random_password())
        return user

    def update(self, instance: models.User, validated_data):
        for (key, value) in validated_data.items():
            if key == 'username':

                users_by_username = User.objects.filter(username=validated_data['username'])
                if users_by_username:
                    user_by_username = users_by_username.get(username=validated_data['username'])
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
        fields = ('user', 'name', 'email', 'gender', 'shoes_size', 'dislikes', 'likes', 'saw', 'bought', 'favourite')

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            if key == 'user':
                user_data = validated_data.get('user')
                if user_data.get('username'):
                    username = user_data['username']
                    phone_code0 = models.PhoneCode.objects.filter(phone=user_data['username'])
                    if phone_code0:  # Если существует этот телефон в проверочной базе
                        phone_code = models.PhoneCode.objects.get(phone=user_data['username'])
                        if phone_code.is_verified:  # Если телефон верифицирован в проверочной базе
                            if models.User.objects.filter(username=username):
                                if int(username) == int(instance.user.username):
                                    phone_code.delete()
                                else:
                                    phone_code.delete()
                                    raise serializers.ValidationError("This phone is already used")
                            else:
                                instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
                        else:
                            raise serializers.ValidationError("This phone is not verified")
                    else:
                        raise serializers.ValidationError("Sms doesn't send to this phone")
                else:
                    instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance


class PhoneCodeSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(min_value=70000000000, max_value=79999999999, required=True)
    code = serializers.IntegerField(min_value=0, max_value=9999, required=False)

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
        fields = ('phone', 'code')


class ShoesSerializer(serializers.ModelSerializer):
    about = serializers.ReadOnlyField()

    class Meta:
        model = models.ShoesItem
        exclude = ('top_material', 'inside_material', 'bottom_material', 'step_material',
                   'country', 'season', 'color', 'zip_type', 'sport_type')


class ShoesShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShoesItem
        fields = ('id', 'image_main', 'name', 'subsubcategory', 'category', 'price', 'brand')


class FilterSerializer(serializers.Serializer):

    class BrandFilterSerializer(serializers.Serializer):
        brand = serializers.ListField(
            child=serializers.CharField()
        )

    class SubsubcategoryFilterSerializer(serializers.Serializer):
        subsubcategory_CHOICES = models.ShoesItem.subsubcategory_CHOICES
        subsubcategory = serializers.ListField(
            child=serializers.ChoiceField(subsubcategory_CHOICES)
        )

    class SubcategoryFilterSerializer(serializers.Serializer):
        subsubcategory_CHOICES = models.ShoesItem.subsubcategory_CHOICES
        subcategory_CHOICES = []
        for i in subsubcategory_CHOICES:
            subcategory_CHOICES.append((i[0], i[0].upper()))
        subcategory_CHOICES = tuple(subcategory_CHOICES)
        subcategory = serializers.ListField(
            child=serializers.ChoiceField(subcategory_CHOICES)
        )
        
    class TopMaterialFilterSerializer(serializers.Serializer):
        top_material_CHOICES = models.ShoesItem.top_material_CHOICES
        top_material = serializers.ListField(
            child=serializers.ChoiceField(top_material_CHOICES)
        )

    class InsideMaterialFilterSerializer(serializers.Serializer):
        inside_material_CHOICES = models.ShoesItem.inside_material_CHOICES
        inside_material = serializers.ListField(
            child=serializers.ChoiceField(inside_material_CHOICES)
        )
        
    class BottomMaterialFilterSerializer(serializers.Serializer):
        bottom_material_CHOICES = models.ShoesItem.bottom_material_CHOICES
        bottom_material = serializers.ListField(
            child=serializers.ChoiceField(bottom_material_CHOICES)
        )
        
    class StepMaterialFilterSerializer(serializers.Serializer):
        step_material_CHOICES = models.ShoesItem.step_material_CHOICES
        step_material = serializers.ListField(
            child=serializers.ChoiceField(step_material_CHOICES)
        )

    class CountryFilterSerializer(serializers.Serializer):
        country_CHOICES = models.ShoesItem.country_CHOICES
        country = serializers.ListField(
            child=serializers.ChoiceField(country_CHOICES)
        )

    class SeasonFilterSerializer(serializers.Serializer):
        season_CHOICES = models.ShoesItem.season_CHOICES
        subcategory = serializers.ListField(
            child=serializers.ChoiceField(season_CHOICES)
        )

    class ColorFilterSerializer(serializers.Serializer):
        color_CHOICES = models.ShoesItem.color_CHOICES
        color = serializers.ListField(
            child=serializers.ChoiceField(color_CHOICES)
        )

    class ZipTypeFilterSerializer(serializers.Serializer):
        zip_type_CHOICES = models.ShoesItem.zip_type_CHOICES
        zip_type = serializers.ListField(
            child=serializers.ChoiceField(zip_type_CHOICES)
        )

    class SportTypeFilterSerializer(serializers.Serializer):
        sport_type_CHOICES = models.ShoesItem.sport_type_CHOICES
        sport_type = serializers.ListField(
            child=serializers.ChoiceField(sport_type_CHOICES)
        )

    class PriceFilterSerializer(serializers.Serializer):
        start_price = serializers.IntegerField()
        end_price = serializers.IntegerField()

    brand_filter = BrandFilterSerializer(required=False)
    subcategory_filter = SubcategoryFilterSerializer(required=False)
    subsubcategory_filter = SubsubcategoryFilterSerializer(required=False)
    season_filter = SeasonFilterSerializer(required=False)
    top_material_filter = TopMaterialFilterSerializer(required=False)
    inside_material_filter = InsideMaterialFilterSerializer(required=False)
    bottom_material_filter = BottomMaterialFilterSerializer(required=False)
    step_material_filter = StepMaterialFilterSerializer(required=False)
    country_filter = CountryFilterSerializer(required=False)
    color_filter = ColorFilterSerializer(required=False)
    zip_type_filter = ZipTypeFilterSerializer(required=False)
    sport_type_filter = SportTypeFilterSerializer(required=False)
    price_filter = PriceFilterSerializer(required=False)


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
