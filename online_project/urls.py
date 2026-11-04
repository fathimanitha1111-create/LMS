from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin site branding
admin.site.site_header = "Online LMS Administration"
admin.site.site_title = "Online LMS Portal"
admin.site.index_title = "Management Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
