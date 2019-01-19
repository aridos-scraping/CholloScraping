from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('list-products',views.listProducts, name='listProducts'),
    path('list-products/<slug:pag_num>',views.listProducts, name='listProducts'),
    path('details/<slug:sku>/',views.details, name='details'),
    path('rate-product/<slug:sku>/<slug:rating>/',views.rateProduct, name='rateProduct'),
    path('refreshWhoosh',views.indexWhoosh, name='indexWhoosh'),
    path('searchWhoosh/',views.searchWhoosh, name='searchWhoosh'),
    path('reloadAll/',views.scrapAllProducts, name='reloadAll'),
    path('reloadMb/',views.scrapMotherboards, name='reloadMb'),
    path('reloadCp/',views.scrapCPUs, name='reloadCp'),
    path('reloadHd/',views.scrapHardDrives, name='reloadHd'),
    path('reloadGc/',views.scrapGraphicCards, name='reloadGc'),
    path('reloadRa/',views.scrapRAM, name='reloadRa'),
    path('reloadLa/',views.scrapLaptops, name='reloadLa'),
    path('reloadGl/',views.scrapGamingLaptops, name='reloadGl'),
    path('reloadSm/',views.scrapSmartphones, name='reloadSm'),
    path('reloadTv/',views.scrapTVs, name='reloadTv'),
    path('insertExamplePrices',views.insertExampleProductPrices, name='insertExamplePrices')
]
