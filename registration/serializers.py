from rest_framework import serializers
from registration.models import Profile, PhoneCode
from django.contrib.auth.models import User
import random
from registration.smsc_api import *


def send_sms(phone, text):
    smsc = SMSC()
    balance = smsc.get_balance()
    print(balance)
    r = smsc.send_sms(str(phone), str(text), sender='DRESS-ME')
    print(r)
    balance = smsc.get_balance()
    print(balance)


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

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if key == 'username':

                users_by_username = User.objects.filter(username=validated_data['username'])
                if users_by_username:
                    user_by_username = users_by_username[0]
                    if user_by_username.username != instance.username:
                        raise serializers.ValidationError("This phone already used")
                    else:
                        setattr(instance, key, value)
                        phone_code = PhoneCode.objects.get(phone=value)
                        phone_code.delete()
                else:
                    setattr(instance, key, value)
                    phone_code = PhoneCode.objects.get(phone=value)
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
        model = Profile
        fields = ('user',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        phone_code0 = PhoneCode.objects.filter(phone=user_data['username'])
        if phone_code0:  # Если существует этот телефон в проверочной базе
            phone_code = PhoneCode.objects.get(phone=user_data['username'])
            if phone_code.is_verified:  # Если телефон верифицирован в проверочной базе
                user = UserSerializer.create(UserSerializer(), validated_data=user_data)
                profile_one = Profile.objects.create(user=user)

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
                    phone_code0 = PhoneCode.objects.filter(phone=user_data['username'])
                    if phone_code0:  # Если существует этот телефон в проверочной базе
                        phone_code = PhoneCode.objects.get(phone=user_data['username'])
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
        valid_phone = PhoneCode.objects.filter(phone=validated_data['phone'])
        if valid_phone:
            phone_code = PhoneCode.objects.get(phone=validated_data['phone'])
            phone_code.code = random.randint(1000, 9999)
            phone_code.save()
            send_sms(phone=validated_data['phone'], text=phone_code.code)
        else:
            code = random.randint(1000, 9999)
            phone_code = PhoneCode.objects.create(phone=validated_data['phone'], code=code)
            phone_code.save()
            send_sms(phone=validated_data['phone'], text=phone_code.code)
        return phone_code

    class Meta:
        model = PhoneCode
        fields = ('phone', 'code', 'is_verified')
