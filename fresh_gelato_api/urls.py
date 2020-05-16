"""fresh_gelato_api URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token

from recipes import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token-auth/', obtain_jwt_token),
    path('api/recipes/', views.recipes_list),
    path('api/recipes/<int:recipe_id>/', views.get_recipe_info),
    path('api/send-email/', views.post_email),
    path('api/current-user/', views.get_current_user),
    url(r'^rest-auth/', include('rest_auth.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

