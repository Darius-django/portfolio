from django.urls import path
from . import views
from .views import contact, success

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success')
]


