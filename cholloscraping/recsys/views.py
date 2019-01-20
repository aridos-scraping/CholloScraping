import shelve
from products.models import Product, Rating
from recsys.forms import ProductForm
from django.shortcuts import render, get_object_or_404
from recsys.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems, topMatches

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.product.sku)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

def loadRS(request):
    loadDict()
    return render(request,'index.html')

def similarProducts(request):
    product = None
    if request.method=='GET':
        form = ProductForm(request.GET, request.FILES)
        if form.is_valid():
            idProduct = form.cleaned_data['id']
            product = get_object_or_404(Product, pk=idProduct)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idProduct),n=6)
            items=[]
            for re in recommended:
                item = Product.objects.get(pk=int(re[1]))
                items.append(item)
            return render(request,'similarProducts.html', {'product': product,'products': items})
    form = ProductForm()
    return render(request,'search_product.html', {'form': form})