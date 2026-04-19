from django.contrib import admin
from django.urls import path, include  # تأكد من استيراد include من django.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('run.urls')),  # الطريقة الصحيحة لربط تطبيق run
    path('accounts/', include('django.contrib.auth.urls')),
]