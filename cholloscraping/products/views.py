from django.shortcuts import render
from django.http import HttpResponse#, JsonReponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from .models import Product, Price
import os.path
import json
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser, OrGroup

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

def scrapAllProducts():
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

def index(request):
	products = Product.objects.all()
	context = {
	    'products': products
	}
	return render(request, 'index.html', context)

def details(request, sku):
	product = Product.objects.get(pk=sku)
	context = {
	    'product': product
	}
	return render(request,'details.html',context)

#Gets all products from DB and makes index
def indexWhoosh(request):
    start_time = time.perf_counter()
    start_cpu = time.process_time()

    schema = Schema(brand=TEXT(stored=True), name=TEXT(stored=True), category=TEXT(stored=True, sortable=True), price=NUMERIC(Decimal,decimal_places=2,stored=True,sortable=True))
    
    if not os.path.exists("whooshdir"):
        os.mkdir("whooshdir")
    ix = create_in("whooshdir",schema)
    writer = ix.writer()

    products = Product.objects.all()
    for product in products:
        #Temporal price model
        writer.add_document(brand=product.brand, name=product.name, category=product.category, price=Price.objects.filter(product=product).reverse()[0].originalPrice)
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
            product_str = r['brand']+" - "+r['name']+" - "+r['category']+" - "+str(r['price'])+"€"
            results_json.append(product_str)
        print('--------------END SEARCH--------------')
        data = json.dumps(results_json)

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)