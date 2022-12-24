
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('income/', include('payment.urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('api.urls')),
]
urlpatterns += static('/static/', document_root=settings.STATIC_ROOT)