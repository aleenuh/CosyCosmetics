from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, CaUser, ShoppingBasket, ShoppingBasketItems, Order, OrderItems
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .permissions import admin_required
from django.core import serializers

class CaUserSignupView(CreateView):
    model = CaUser
    form_class = CASignupForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class AdminSignupView(CreateView):
    model = CaUser
    form_class = AdminSignupForm
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class Login(LoginView):
    template_name = 'login.html'

def logout_view(request):
    logout(request)
    return redirect('/')

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def all_products(request):
    all_p = Product.objects.all()
    flag = request.GET.get('format', '')
    if flag == "json":
        serialised_products = serializers.serialize("json", all_p)
        return HttpResponse(serialised_products, content_type="application/json")
    else:
        return render(request, 'all_products.html', {'products': all_p})

def singleproduct(request, prodid):
    prod = get_object_or_404(Product, pk=prodid)
    return render(request, 'single_product.html', {'product': prod})

@login_required
@admin_required
def myForm(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            return render(request, 'single_product.html', {'product': new_product})
        else:
            form = ProductForm()
            return rener(request, 'forms.html', {'form':form})

def addproducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            return render(request, 'single_product.html', {'product': new_product})
    else:
        form = ProductForm()
        return render(request, 'forms.html', {'form': form})

@login_required
def add_to_basket(request, prodid):
    user = request.user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        shopping_basket = ShoppingBasket(user_id=user).save()

    # get shopping basket
    product = Product.objects.get(pk=prodid)
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=product.id).first()
    if sbi is None:
        sbi = ShoppingBasketItems(basket_id=shopping_basket, product_id=product.id).save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return render(request, 'single_product.html', {'product': product, 'added': True})

'''@login_required
def get_basket(request):
    user = request.user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        shopping_basket = ShoppingBasket(user_id=user).save()
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    return render(request, 'shopping_basket.html', {'basket':shopping_basket, 'items':sbi})

@login_required
def remove_from_basket(request, sbi):
    sb = ShoppingBasketItems.objects.get(pk=sbi).delete()
    return redirect('/basket')'''

@login_required
def order_form(request):
    user = request.user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        return redirect(request, '/')
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    if request.method == 'POST':
        form = OrderForm\
            (request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user
            order.save()
            order_items = []
            for basketitem in sbi:
                order_item = OrderItems(order_id=order, product_id=basketitem.product, quantity=basketitem.quantity)
                order_items.append(order_item)
            shopping_basket.delete()
            return render(request, 'ordercomplete.html', {'order':order, 'items':order_items})
        else:
            form = OrderForm()
            return render(request, 'orderform.html', {'form':form, 'basket':shopping_basket, 'items':sbi})

