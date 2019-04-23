"""
Rotas do likebee.

Arquivo com todas as rotas da aplicacao.
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from controlcenter.views import controlcenter

from .core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),
    path('summernote/', include('django_summernote.urls')),
    path('app/', admin.site.urls),
    path('app/dashboard/', controlcenter.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if hasattr(settings, 'ADMIN_SITE_HEADER'):
    admin.site.site_header = settings.ADMIN_SITE_HEADER
    admin.site.site_title = settings.ADMIN_SITE_HEADER

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
