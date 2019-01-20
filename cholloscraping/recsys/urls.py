from django.urls import path

from . import views


urlpatterns = [
    path('loadRS', views.loadRS, name="loadRS"),
    path('similarProducts', views.similarProducts, name='similarProducts'),
]