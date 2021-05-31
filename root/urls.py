from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='name=root-home'),
    path('images/', views.images, name='name=root-images'),
    path('dashboard/', views.dashboard, name='name=root-dashboard'),
    path('internal/', views.internal, name='name=root-internal'),
    path('blog/', views.blog, name='name=root-blog')

]