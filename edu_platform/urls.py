from django.contrib import admin
from django.urls import path, include
from edu1.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('manage_roles/', include('edu1.urls')),
]
