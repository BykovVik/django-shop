from django.shortcuts import render, get_list_or_404
from .models import Category, Product
from cart.form import CartAddProductForm

def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_list_or_404(Category, slug=category_slug)
        products = products.filter(category=category[0])
    
    return render(
        request,
        'shop/product/list.html',
        {
            'category' : category,
            'categories' : categories,
            'products': products
        }
    )

def product_detail(request, id, slug):

    product = get_list_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product[0],
            'cart_product_form': cart_product_form
        }
    )

