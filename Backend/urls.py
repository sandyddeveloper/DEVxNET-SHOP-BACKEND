from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Analytics/', include("Analytics.urls")),
    path('Customer/', include('Customer.urls')),
    path('Store/', include('Store.urls')),
    path('', include('UserAuth.urls')),
    path('Vendor/', include('Vendor.urls')),
    path('Bot/', include('Bot.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


