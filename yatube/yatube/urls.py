from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('about/', include('about.urls', namespace='about')),
    path('auth/', include('django.contrib.auth.urls'))
]

handler404 = 'core.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
