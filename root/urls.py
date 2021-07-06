from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='name=root-home'),
    path('images/', views.images, name='name=root-images'),
    path('internal/', views.internal, name='name=root-internal'),
    path('blog/', views.blog, name='name=root-blog'),
    path('login/', auth_views.LoginView.as_view(template_name='root/login.html'), name='name=root-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='root/logout.html'), name='name=root-logout')
]
