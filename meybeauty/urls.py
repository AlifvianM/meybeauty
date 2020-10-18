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
from django.urls import path, include, re_path
# from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
from users.forms import MyLoginView
from django.contrib.auth import views as auth_views
from django.views.static import serve 



urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
	path('', include('shop.urls')),
    re_path(r'^accounts/',include('allauth.urls')),
    path('adminpage/', include('adminpage.urls')),
    path('admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    # path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    # path('register/', users_views.register, name='register'),
    path('register/', users_views.signup, name='register'),

    # path('login/', MyLoginView.as_view(template_name = 'users/login-register.html'), name='login'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', users_views.activate, name='activate'),
    path('register/success/', users_views.register_success, name = 'register_success'),
    path('login/', users_views.login_view, name= 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/login-register.html'), name='logout'),
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




