from django.urls import path
from articles import views

urlpatterns = [
    path('main', views.get_main),
]

