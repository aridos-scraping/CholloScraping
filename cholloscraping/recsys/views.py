import shelve
from products.models import Product, Rating
from django.contrib.auth.models import User
from recsys.forms import UserForm, ProductForm
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
    msg = 'Matriz RecSys cargada correctamente'
    return render(request, 'message.html', {'message': msg})

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

def recommendedProducts(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(User, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:3]
            items = []
            for re in recommended:
                item = Product.objects.get(pk=re[1])
                items.append(item)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})