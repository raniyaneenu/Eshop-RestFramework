from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns=[
    path('category',views.CategoryClassView.as_view({'post':'create','get':'listing'}),name='category'),
    path('category/<id>',views.CategoryClassView.as_view({'delete':'delete'}),name='category'),
    path('product',views.ProductClassView.as_view({'post':'create','get':'listing'}),name='category'),
    path('product/<id>',views.ProductClassView.as_view({'put':'edit','delete':'delete'}),name='category'),

    path("login", views.LoginUser.as_view(), name="login"),
    path("refresh", jwt_views.TokenRefreshView.as_view(), name="refresh"),
    path("logout", views.LogoutView.as_view({"post": "create"}), name="logout"),

]