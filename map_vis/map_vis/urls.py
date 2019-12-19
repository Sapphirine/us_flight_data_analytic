from django.conf.urls import url
from django.urls import path
from . import view

urlpatterns = [
    path('map', view.map),
    path('predict', view.predict),
    path('home', view.home)
]
