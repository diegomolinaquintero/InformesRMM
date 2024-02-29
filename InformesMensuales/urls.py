from django.urls import path
from .views import  dashboard, exit

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('exit/', exit, name='exit')
]