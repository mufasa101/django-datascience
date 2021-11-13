from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import login_view, logout_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sales.urls', namespace="sales")),
    path('reports/', include('reports.urls', namespace="reports")),
    path('profile/', include('profiles.urls', namespace="profile")),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]


# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()