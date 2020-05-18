from django.contrib import admin
from django.urls import path
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
    path('api/user/', views.user_view)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

