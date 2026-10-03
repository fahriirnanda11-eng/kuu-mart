from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from store.views import service_worker



urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'admin/',
        admin.site.urls
    ),


    # =====================================================
    # SERVICE WORKER
    # =====================================================

    path(
        'service-worker.js',
        service_worker,
        name='service_worker'
    ),


    # =====================================================
    # STORE
    # =====================================================

    path(
        '',
        include('store.urls')
    ),


    # =====================================================
    # ACCOUNTS
    # =====================================================

    path(
        '',
        include('accounts.urls')
    ),

]


# =========================================================
# MEDIA
# =========================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )