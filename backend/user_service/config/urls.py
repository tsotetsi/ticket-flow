from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api.views import RegisterView, UserProfileView


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # API base url.
    path('api/', include("config.api_router")),
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/profile', UserProfileView.as_view(), name='profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve static files directly if we are in development.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)