from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from axaxa.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('axaxa.urls')),
    path('', include('api_v1.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

