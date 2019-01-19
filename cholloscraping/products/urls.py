from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('list-products',views.listProducts, name='listProducts'),
    path('list-products/<slug:pag_num>',views.listProducts, name='listProducts'),
    path('details/<slug:sku>/',views.details, name='details'),
    path('rate-product/<slug:sku>/<slug:rating>/',views.rateProduct, name='rateProduct'),
    path('refreshWhoosh/',views.indexWhoosh, name='indexWhoosh'),
    path('searchWhoosh/',views.searchWhoosh, name='searchWhoosh'),

    ############## RELOAD PRODUCTS URLS ####################################
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

    ############## LIST PRODUCTS URLS ####################################
    path('listAll/',views.listAllProducts, name='listAll'),
    path('listAll/<slug:pag_num>',views.listAllProducts, name='listAll'),
    path('listMb/',views.listMotherboards, name='listMb'),
    path('listMb/<slug:pag_num>',views.listMotherboards, name='listMb'),
    path('listCp/',views.listCPUs, name='listCp'),
    path('listCp/<slug:pag_num>',views.listCPUs, name='listCp'),
    path('listHd/',views.listHardDrives, name='listHd'),
    path('listHd/<slug:pag_num>',views.listHardDrives, name='listHd'),
    path('listGc/',views.listGraphicCards, name='listGc'),
    path('listGc/<slug:pag_num>',views.listGraphicCards, name='listGc'),
    path('listRa/',views.listRAM, name='listRa'),
    path('listRa/<slug:pag_num>',views.listRAM, name='listRa'),
    path('listLa/',views.listLaptops, name='listLa'),
    path('listLa/<slug:pag_num>',views.listLaptops, name='listLa'),
    path('listGl/',views.listGamingLaptops, name='listGl'),
    path('listGl/<slug:pag_num>',views.listGamingLaptops, name='listGl'),
    path('listSm/',views.listSmartphones, name='listSm'),
    path('listSm/<slug:pag_num>',views.listSmartphones, name='listSm'),
    path('listTv/',views.listTVs, name='listTv'),
    path('listTv/<slug:pag_num>',views.listTVs, name='listTv'),
    
    path('insertExamplePrices',views.insertExampleProductPrices, name='insertExamplePrices')
]
