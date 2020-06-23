"""meybeauty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
from users.forms import MyLoginView
from django.contrib.auth import views as auth_views



urlpatterns = [
	path('', include('shop.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('register/', users_views.register, name='register'),
    # path('login/', MyLoginView.as_view(template_name = 'users/login-register.html'), name='login'),
    path('login/', users_views.login_view, name= 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/login-register.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)