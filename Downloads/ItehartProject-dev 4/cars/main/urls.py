
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('health', views.change),
    path('health/', views.change_red),
    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    #path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/signin',views.signin),
    path('users/signup', views.SignUp.as_view())
]
