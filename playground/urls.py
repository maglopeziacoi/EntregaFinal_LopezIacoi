from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pages.views import HomeView, AboutView
from accounts.views import public_profile

urlpatterns = [
path('admin/', admin.site.urls),

path('', HomeView.as_view(), name='home'),
path('about/', AboutView.as_view(), name='about'),

path('pages/', include('pages.urls')),
path('accounts/', include('accounts.urls')),
path('accounts/', include('django.contrib.auth.urls')),
path('messages/', include('messenger.urls')),
path('about/<str:username>/', public_profile, name='public_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)