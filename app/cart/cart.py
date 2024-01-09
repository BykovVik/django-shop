from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:

    def __init__(self, request) -> None:
        """
        Cart init
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session.get(settings.CART_SESSION_ID)

        self.cart = cart

    def __iter__(self):
        """
        Loops through the shopping cart items and receives goods from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product in cart
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Marked the session as "modified" to ensure it is saved
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove item from cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        Remove cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()