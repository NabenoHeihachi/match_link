from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app_document.urls')),
    path('app/account/', include('app_account.urls')),
    path('app/profile/', include('app_profile.urls')),
    path('app/matching/', include('app_matching.urls')),
    path('app/system-manager/admin-site/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)