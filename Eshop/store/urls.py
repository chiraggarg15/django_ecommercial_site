from .views import sign,Login,Index
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# from ./settings import MEDIA_ROOT,MEDIA_URL.
from django.conf import settings
urlpatterns = [
    path('admin/',admin.site.urls),
    path('',Index.as_view(),name='homepage'),
    path('signup',sign),
    path('login',Login.as_view())
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
