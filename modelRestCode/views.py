from django.shortcuts import render
from accounts import models as acc 
from cart import models as ct 
from shop import models as shp 

from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, OpenApiParameter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db.models import Q
from . import serializers
from . import functions

from django.contrib.auth.models import User,auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import time
from dateutil.relativedelta import relativedelta
from datetime import date,timedelta
from django.conf import settings
import datetime
# Create your views here.

class CategoryClassView(GenericViewSet):
    @extend_schema(
    tags=['category'],
    request   = serializers.categorySerializer,
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def create(self, request):
        serializer=serializers.categorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(data={"data":serializer.data,"message": "created",'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        except exceptions.ExistsError as e:
            return Response(data={"data": e.message, 'status':status.HTTP_409_CONFLICT}, status=status.HTTP_409_CONFLICT)

    @extend_schema(
    tags=['category'],
    request   = serializers.categorySerializer,
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def listing(self, request):
        data=shp.categ.objects.all()
        serializer=serializers.categorySerializer(data,many=True)
        return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
        
    @extend_schema(
    tags=['category'],
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def delete(self, request,id):
        data=shp.categ.objects.get(id=id)
        data.delete()
        return Response(data={"data":"deleted"}, status=status.HTTP_200_OK)




class ProductClassView(GenericViewSet):
    pagination_class = LimitOffsetPagination
    @extend_schema(
    tags=['product'],
    request   = serializers.ProductSeralizer,
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def create(self, request):
        serializer=serializers.ProductSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(data={"data":serializer.data,"message": "created",'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        except exceptions.ExistsError as e:
            return Response(data={"data": e.message, 'status':status.HTTP_409_CONFLICT}, status=status.HTTP_409_CONFLICT)
    
    @extend_schema(
    tags=['product'],
    request   = serializers.ProductViewSeralizer,
    parameters=[

            OpenApiParameter(name='limit', required=False, type=int,location=OpenApiParameter.QUERY),
            OpenApiParameter(name='offset', required=False, type=int,location=OpenApiParameter.QUERY),
            OpenApiParameter(name='search_key', required=False, location=OpenApiParameter.QUERY),

            ],
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def listing(self, request):
        search_key = request.query_params.get('search_key')
        data=shp.categ.objects.all()
        if search_key:
            data=data.filter(name__icontains=search_key)
        
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(data,request)
        serializer=serializers.ProductViewSeralizer(result_page,many=True)
        # return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
        return paginator.get_paginated_response({"Data":serializer.data,"message":"Success","Status":"200"})

    @extend_schema(
    tags=['product'],
    request   = serializers.ProductSeralizer,
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def edit(self, request,id):
        serializer=serializers.ProductSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        edit_data=functions.edit_categ(id,serializer.data)
        return Response(data={"data":serializer.data}, status=status.HTTP_202_ACCEPTED)
    
    @extend_schema(
    tags=['product'],
    responses = {201: dict,
            404: dict,
            409: dict})
    
    def delete(self, request,id):
        data=shp.products.objects.get(id=id)
        data.delete()
        return Response(data={"data":"deleted"}, status=status.HTTP_200_OK)
        

class LoginUser(APIView):
    
    authentication_classes = [] #disables authentication    
    permission_classes = []
    @extend_schema(
        request   = serializers.LoginSerializer,
        responses = {
            200: dict,
            400: dict
        }
    )
    def post(self,request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        remember_me = serializer.validated_data.get('remember_me')
        response = Response()
        if (username is None) or (password is None):
            return Response(data={"detail":"username and password required"}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.filter(username__iexact=username).first()
        if(user is None):
            return Response(data={"detail":"No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

        if (not user.check_password(password)):
            return Response(data={"detail":"No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response(data={"detail":'You have not activated your account yet'}, status=status.HTTP_404_NOT_FOUND)
        
        def get_token(user):
            return RefreshToken.for_user(user) 
        data={}
        refresh = get_token(user)
        
        data['refresh'] = str(refresh)
        a =data['access'] = str(refresh.access_token)

        if remember_me == True:

            token_decode = jwt.decode(a, key=settings.SECRET_KEY, algorithms=['HS256', ])
            
            ad = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(token_decode["exp"]))

            datetime_object = datetime.datetime.strptime(ad, '%Y-%m-%d %H:%M:%S')
            exte_date = datetime_object + relativedelta(months=+3)

            token_decode.update({"exp": int(exte_date.timestamp())})
            
            final_enc = jwt.encode(token_decode, key=settings.SECRET_KEY, algorithm='HS256')

            data.update({"access": final_enc})

        
        return Response(data=data)

class LogoutView(GenericViewSet):
    """
    API for Logout.
    """

    @extend_schema(
        request   = serializers.LogoutSerializer,
        responses = {
            200:dict
        }
    
    )

    def create(self, request):
        """Logout an user account.
        Args:
            refresh: refresh token to be blacklisted.
        Returns:
            Response: status of the user logout.
        """
        serializer = serializers.LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.blacklist_token(serializer.validated_data)

        return Response(data={"detail": "Logout success."}, status=status.HTTP_200_OK)
