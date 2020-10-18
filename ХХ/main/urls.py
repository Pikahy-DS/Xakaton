from django.urls import path, include
from . import views
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'home'),
    path('about',views.about, name = 'about')
] +static(settings.STATIC_URL, document_root = settings.STATIC_URL)