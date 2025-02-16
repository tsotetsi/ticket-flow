from allauth.account.views import confirm_email, email_verification_sent
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django_prometheus import exports

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from users.api.views import RegisterView, UserProfileView, VerifyEmailView


urlpatterns = [
    # Django based views.
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # API BASE URL For Authentication JWT.
    path('api/', include("config.api_router")),
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/account-confirm-email/<str:key>/', confirm_email , name='account_confirm_email'),
    path('api/account-email-verification-sent', email_verification_sent, name='account_email_verification_sent'),
    path('api/profile', UserProfileView.as_view(), name='profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    # JSON Schema endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Optional: Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Optional: ReDoc
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += [
    path('metrics/', exports.ExportToDjangoView, name='prometheus-django-metrics'),
]

# Serve static files directly if we are in development.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
    ]