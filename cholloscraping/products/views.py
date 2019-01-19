from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from .models import Product, Price, Rating
import os.path
from math import ceil
import json
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser, OrGroup
import random

category_map = {
    'Motherboards':'&order=relevance&gtmTitle=Placas%20Base&idFamilies%5B%5D=3',
    'CPUs':'&order=relevance&gtmTitle=Procesadores%20para%20el%20PC&idFamilies%5B%5D=4',
    'HardDrives': '&order=relevance&gtmTitle=Discos%20Duros&idFamilies%5B%5D=5',
    'GraphicCards':'&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6',
    'RAM':'&order=relevance&gtmTitle=Memorias%20RAM&idFamilies%5B%5D=7',
    'Laptops':'&order=relevance&gtmTitle=Port%C3%A1tiles&idFamilies%5B%5D=1115',
    'GamingLaptops':'&order=relevance&gtmTitle=Port%C3%A1tiles%20Gaming&idFamilies%5B%5D=1115',
    'Smartphones':'&order=relevance&gtmTitle=M%C3%B3viles%20libres%20y%20Smartphones&idFamilies%5B%5D=1116',
    'TVs':'&order=relevance&gtmTitle=Televisores&idFamilies%5B%5D=1179'
}

def scrapeProductsByCategory(category):
    category_page = category_map[category]
    npages = 0
    i = 0
    #Max refreshes whenever a page has articles
    max = 1

    while i<max:
        #The first page index = 0
        #Ej: https://www.pccomponentes.com/listado/ajax?page=3&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6
        actual_page = "https://www.pccomponentes.com/listado/ajax?page=" + str(i) + category_page
        req = Request(actual_page, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "lxml")
        i = i+1
        l = soup.find_all("article", class_="tarjeta-articulo")
        if len(l)!=0:
            npages = npages+1
            print("Page: "+str(i-1))        
            max = max+1
            for a in l:
                sku = a.find_all("meta", itemprop="sku")[0]["content"]
                print("SKU: " + sku)

                brand = a.find_all("meta", itemprop="brand")[0]["content"]
                print("BRAND: " + brand)

                image = a.find_all("img", itemprop="image")[0]["src"]
                imageUrl = "https:" + str(image)
                print("IMAGE: " + imageUrl)

                name = a.find_all("a", itemprop="url")[0]["data-name"]
                print("NAME: " + name)

                category = a.find_all("a", itemprop="url")[0]["data-category"]
                print("CATEGORY: " + category)

                currentPrice = a.find_all("a", itemprop="url")[0]["data-price"]
                print("CURRENT PRICE: " + currentPrice)

                originalPrice = a.find_all("meta", itemprop="price")[0]["content"]
                print("ORIGINAL PRICE: " + originalPrice)

                product = Product(sku=sku,brand=brand,image=image,name=name,category=category)
                product.save()

                price = Price(originalPrice=originalPrice,currentPrice=currentPrice,product=product)
                price.save()
                print("-----------------------")
        else:
            print("There is no more products for this category, pages registered in total: {}".format(npages))
            print("-----------------------")    


############################################ SCRAPING PRODUCTS #############################################################
############################################################################################################################
def scrapAllProducts(request):
    start_time = time.perf_counter()
    start_cpu = time.process_time()

    for category in category_map:
        scrapeProductsByCategory(category)

    end_time = time.perf_counter()
    end_cpu = time.process_time()

    #Time spent in total
    print("Elapsed time: {0:.3f} (s)".format(end_time-start_time))
    #Time spent only CPU    
    print("CPU process time: {0:.3f} (s)".format(end_cpu-start_cpu))

    return HttpResponse('Se han insertado {} productos en {} segundos'.format(Product.objects.count(),end_time-start_time))

def scrapMotherboards(request, pag_num=1):
    scrapeProductsByCategory("Motherboards")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Placas Base')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listMb'
    }
    return render(request, 'list-products.html', context)

def scrapCPUs(request, pag_num=1):
    scrapeProductsByCategory("CPUs")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Procesadores')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listCp'
    }
    return render(request, 'list-products.html', context)

def scrapHardDrives(request, pag_num=1):
    scrapeProductsByCategory("HardDrives")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Discos Duros')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listHd'
    }
    return render(request, 'list-products.html', context)

def scrapGraphicCards(request, pag_num=1):
    scrapeProductsByCategory("GraphicCards")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Tarjetas Gráficas')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listGc'
    }
    return render(request, 'list-products.html', context)

def scrapRAM(request, pag_num=1):
    scrapeProductsByCategory("RAM")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Memorias RAM')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listRa'
    }
    return render(request, 'list-products.html', context)

def scrapLaptops(request, pag_num=1):
    scrapeProductsByCategory("Laptops")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Portátiles')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listLa'
    }
    return render(request, 'list-products.html', context)

def scrapGamingLaptops(request, pag_num=1):
    scrapeProductsByCategory("GamingLaptops")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Portátiles Gaming')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listGl'
    }
    return render(request, 'list-products.html', context)

def scrapSmartphones(request, pag_num=1):
    scrapeProductsByCategory("Smartphones")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Smartphone/Móviles')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listSm'
    }
    return render(request, 'list-products.html', context)

def scrapTVs(request, pag_num=1):
    scrapeProductsByCategory("TVs")
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Televisores')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listTv'
    }
    return render(request, 'list-products.html', context)


############################################ LISTING PRODUCTS #############################################################
############################################################################################################################
def listAllProducts(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.all()[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listAllProducts'
    }
    return render(request, 'list-products.html', context)

def listMotherboards(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Placas Base')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Placas Base').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listMb'
    }
    return render(request, 'list-products.html', context)

def listCPUs(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Procesadores')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Procesadores').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listCp'
    }
    return render(request, 'list-products.html', context)

def listHardDrives(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Discos Duros')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Discos Duros').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listHd'
    }
    return render(request, 'list-products.html', context)

def listGraphicCards(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Tarjetas Gráficas')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Tarjetas Gráficas').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listGc'
    }
    return render(request, 'list-products.html', context)

def listRAM(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Memorias RAM')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Memorias RAM').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listRa'
    }
    return render(request, 'list-products.html', context)

def listLaptops(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Portátiles')[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listLa'
    }
    return render(request, 'list-products.html', context)

def listGamingLaptops(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Portátiles Gaming')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Portátiles Gaming').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listGl'
    }
    return render(request, 'list-products.html', context)

def listSmartphones(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Smartphone/Móviles')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Smartphone/Móviles').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listSm'
    }
    return render(request, 'list-products.html', context)

def listTVs(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.filter(category='Televisores')[first-1:top]
    total_pages = ceil(Product.objects.filter(category='Televisores').count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/listTv'
    }
    return render(request, 'list-products.html', context)

#This will be called listMostRatedProducts in the future
def listProducts(request, pag_num=1):
    top = int(pag_num)*12
    first = top-11
    products = Product.objects.all()[first-1:top]
    total_pages = ceil(Product.objects.count()/12)
    context = {
        'products': products,
        #Variables para paginacion
        'pag_num': int(pag_num),
        'total_pages': total_pages,
        'range': range(1, total_pages+1),
        'redirect_uri': '/products/list-products'
    }
    return render(request, 'list-products.html', context)

def details(request, sku):
    product = Product.objects.get(pk=sku)
    prices = Price.objects.filter(product__sku=sku)
    rating = None
    productRating = Rating.objects.filter(product=product, user=request.user).first()
    
    if(productRating!=None):
        rating = str(productRating.rating)
    context = {
        'product': product,
        'prices': prices,
        'rating': rating
    }
    return render(request,'details.html',context)

def rateProduct(request, sku, rating):
    product = Product.objects.get(pk=sku)

    productRating = Rating.objects.filter(product=product, user=request.user).first()
    if(productRating==None):
        productRating = Rating(product=product, user=request.user, rating=rating)
        productRating.save()
    else:
        productRating.rating = rating
        productRating.save()

    prices = Price.objects.filter(product__sku=sku)
    context = {
        'product': product,
        'prices': prices,
        'rating': productRating.rating
    }
    return render(request,'details.html',context)

#Gets all products from DB and makes index
def indexWhoosh(request):
    start_time = time.perf_counter()
    start_cpu = time.process_time()

    schema = Schema(sku=NUMERIC(stored=True), image=STORED(), brand=TEXT(stored=True), name=TEXT(stored=True),
                    category=TEXT(stored=True, sortable=True), price=NUMERIC(Decimal,decimal_places=2,stored=True,sortable=True))
    
    if not os.path.exists("whooshdir"):
        os.mkdir("whooshdir")
    ix = create_in("whooshdir",schema)
    writer = ix.writer()

    products = Product.objects.all()
    for product in products:
        writer.add_document(sku=product.sku, image="http:"+product.image, brand=product.brand, name=product.name, 
                            category=product.category, price=Price.objects.filter(product=product).reverse()[0].originalPrice)
    writer.commit()

    end_time = time.perf_counter()
    end_cpu = time.process_time()

    #Time spent in total
    print("Elapsed time: {0:.3f} (s)".format(end_time-start_time))
    #Time spent only CPU    
    print("CPU process time: {0:.3f} (s)".format(end_cpu-start_cpu))

    return HttpResponse('{} products indexed in {}'.format(len(products),end_time-start_time))

#Search-whoosh products by query
def searchWhoosh(request):
    ix = open_dir("whooshdir")
    qp = MultifieldParser(['brand','name','category','price'], schema=ix.schema, group=OrGroup)
    
    q = qp.parse(request.GET.get('query'))

    with ix.searcher() as searcher:
        #Gets the top X results for the query where X=query_limit
        results = searcher.search(q,limit=int(request.GET.get('query_limit')))
        print("{} products".format(len(results)))
        results_json = []
        for r in results:
            #product = r['brand']+" - "+r['name']+" - "+r['category']+" - "+str(r['price'])+"€"
            product = [r['sku'], r['image'], r['brand'], r['name'], r['category'], r['price']]
            results_json.append(product)
        print('--------------END SEARCH--------------')
    print(results_json)
    mimetype = 'application/json'
    return HttpResponse(json.dumps(results_json), mimetype)

def insertExampleProductPrices(request):
    products = Product.objects.all()
    for p in products:
        # Adds new random price to product
        actualPrice = Price.objects.filter(product=p).reverse()[0].originalPrice
        randomPrice = actualPrice+random.randint(1,51)
        newPrice = Price(originalPrice=randomPrice, currentPrice=randomPrice, product=p)
        newPrice.save()
        print(p.name+" - "+str(actualPrice)+" -> "+str(randomPrice))
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')