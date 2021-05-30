from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='name=welcome-home'),
    path('images/', views.images, name='name=welcome-images'),
    path('dashboard/', views.dashboard, name='name=welcome-dashboard'),
    path('internal/', views.internal, name='name=welcome-internal'),

]