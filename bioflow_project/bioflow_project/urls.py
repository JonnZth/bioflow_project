from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('reagents/', include('reagents.urls')),
    path('equipments/', include('equipments.urls')),
    path('schedules/', include('schedules.urls')),
    path('protocols/', include('protocols.urls')),
    path('samples/', include('samples.urls')),
    path('experiments/', include('experiments.urls')),
    path('analysis/', include('analysis.urls')),
    path('inventory/', include('inventory.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
