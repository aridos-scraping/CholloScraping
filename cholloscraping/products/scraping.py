from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


paginas = []
i=0
max=20
while i<=max:
    paginas.append("https://www.pccomponentes.com/listado/ajax?page=" + str(i) + "&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6")
    i= i+1

for pagina in paginas:
    req = Request(pagina, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")    
    l = soup.find_all("article", class_="tarjeta-articulo")

    for i in l:
        sku = i.find_all("meta", itemprop="sku")[0]["content"]
        print("SKU:" + sku)

        brand = i.find_all("meta", itemprop="brand")[0]["content"]
        print("BRAND:" + brand)

        image = i.find_all("img", itemprop="image")[0]["src"]
        imageUrl = "https:" + str(image)
        print("IMAGE:" + imageUrl)

        name = i.find_all("a", itemprop="url")[0]["data-name"]
        print("NAME: " + name)

        category = i.find_all("a", itemprop="url")[0]["data-category"]
        print("CATEGORY: " + category)

        currentPrice = i.find_all("a", itemprop="url")[0]["data-price"]
        print("CURRENT PRICE: " + currentPrice)

        originalPrice = i.find_all("meta", itemprop="price")[0]["content"]
        print("ORIGINAL PRICE: " + originalPrice)


        print("-----------------------")

