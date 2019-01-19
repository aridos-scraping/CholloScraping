from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('list-products',views.listProducts, name='listProducts'),
    path('list-products/<slug:pag_num>',views.listProducts, name='listProducts'),
    path('details/<slug:sku>/',views.details, name='details'),
    path('rate-product/<slug:sku>/<slug:rating>/',views.rateProduct, name='rateProduct'),
    path('refreshWhoosh/',views.indexWhoosh, name='indexWhoosh'),
    path('searchWhoosh/',views.searchWhoosh, name='searchWhoosh')
]
