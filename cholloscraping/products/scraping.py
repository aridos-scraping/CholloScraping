from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getGraphicCards():
    npages = 0
    i = 0
    #Max refreshes whenever a page has articles
    max = 1

    while i<max:
        #The first page index = 0
        #Ej: https://www.pccomponentes.com/listado/ajax?page=3&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6
        actual_page = "https://www.pccomponentes.com/listado/ajax?page=" + str(i) + "&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6"
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

                print("-----------------------")
        else:
            print("There is no more products, pages registered in total: {}".format(npages))
            print("-----------------------")

getGraphicCards()