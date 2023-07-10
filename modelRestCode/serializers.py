from rest_framework import serializers
from accounts import models as acc 
from cart import models as ct 
from shop import models as shp 
from django.template.defaultfilters import slugify
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

class categorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model=shp.categ 
        fields="__all__"


class ProductSeralizer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model=shp.products
        fields="__all__"

class ProductViewSeralizer(serializers.ModelSerializer):
    class Meta:
        model=shp.products
        fields=['id','slug','name']

class LoginSerializer(serializers.Serializer): 

    username =serializers.CharField(min_length=2, max_length=50, required=True)
    password = serializers.CharField(min_length=1, max_length=50, required=True)
    remember_me = serializers.BooleanField(default=False, required=False)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(min_length=100, max_length=300, required=True)

    def validate_refresh(self, refresh):
        try:
            token = RefreshToken(refresh)
        except TokenError:
            raise TokenError
        return token

    def blacklist_token(self, validated_data):
        token = validated_data.get("refresh")
        token.blacklist()