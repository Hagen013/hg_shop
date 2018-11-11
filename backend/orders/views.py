from django.views.generic import TemplateView


class OrderView(TemplateView):
    template_name = 'pages/order_page.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(OrderView, self).get_context_data(**kwargs)
    #     cart = Cart(self.request.session)
    #     context['cart'] = cart
    #     context['OrderForm'] = OrderForm()
    #     return context


# def OrderCreate(request):
#     cart = Cart(request.session)
#     if request.method == 'POST':
#         city = request.POST['adress']
#         if city == '':
#             city = 'Москва'
#         form = OrderForm(request.POST)

#         if form.is_valid():
#             order = form.save()
            
#             for item in cart.items:
#                 order_item = OrderItem(
#                     order=order,
#                     product=item.product,
#                     price=item.price,
#                     quantity=item.quantity,
#                 )
#                 order_item.save()



#             UserOrderNotification.apply_async((order.pk,), countdown=10)
#             AdminOrderNotification.apply_async((order.pk,), countdown=10)
#             cart.clear()

#             return redirect('order:success')
#         else:
#             return redirect('order:View')


class OrderSuccessView(TemplateView):
    template_name = 'pages/order_success.html'


class OrderCancelledView(TemplateView):
    template_name = 'pages/order_cancelled.html'
