from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse

from core.models import ProductPage
from .cart import Cart


@require_POST
def Add(request):
    cart = Cart(request.session)
    if request.is_ajax():
        print(request.POST)
        cart = Cart(request.session)
        product_id = request.POST.get('add_item_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(ProductPage, id=product_id)
        cart.add(
            product=product,
            price=product.price,
            quantity=quantity,
        )
        return HttpResponse('Item added to cart')
    else:
        return redirect('cart:Details')


@require_POST
def Update(request):
    if request.is_ajax():
        cart = Cart(request.session)
        product_id = request.POST['update_item_id']
        product = get_object_or_404(ProductPage, id=product_id)
        quantity = request.POST['quantity']
        cart.set_quantity(product, quantity)

        subtotal = cart._items_dict[product.pk].subtotal
        total = cart.total_price
        count = cart.count

        return JsonResponse({
            'id': product_id,
            'subtotal': subtotal,
            'total': total,
            'count': count,
        })
    else:
        return redirect('cart:default')


@require_POST
def Remove(request, product_id):
    cart = Cart(request.session)
    product = get_object_or_404(ProductPage, id=product_id)
    cart.remove(product)
    return redirect('cart:default')


class CartDetailView(TemplateView):
    template_name = 'pages/cart_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        cart = Cart(self.request.session)
        context['cart'] = cart
        return context

@require_GET
def CartInfo(request):
    if request.is_ajax():
        cart = Cart(request.session)
        is_empty = cart.is_empty
        count = cart.count
        return JsonResponse({
            'is_empty': is_empty,
            'count': count,
            'total': cart.total_price,
        })
    else:
        redirect('cart:default')
