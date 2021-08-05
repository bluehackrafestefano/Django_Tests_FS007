from django.urls import path
from .views import home, hash, quickhash

urlpatterns = [
    path('', home, name='home'),
    path('hash/<str:hash>', hash, name="hash"),
    path('quickhash', quickhash, name='quickhash'),
]