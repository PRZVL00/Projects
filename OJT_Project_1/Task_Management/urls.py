from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client_home', views.client_home, name='client_home'),
    path('client_pending', views.client_pending, name='client_pending'),
]
