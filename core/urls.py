from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminApp/', include('adminApp.urls')),
    path('',include('users.urls')),
    path('tests/',include("tests.urls")),
    path('api/',include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


