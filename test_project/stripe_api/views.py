from django.shortcuts import render, redirect
from stripe_api.models import Item, Order
from stripe_api.forms import OrderForm
from django.conf import settings
import stripe, os


def buy_id(request, id):
    '''Покупка одного товараю'''

    stripe.api_key = settings.STRIPE_TEST_SKEY
    item = Item.objects.get(id = id)
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                'price' : item.stripe_price_id,
                'quantity' : 1,
            },
        ],
        mode = "payment",
        success_url = os.environ.get('success_url'),
		#return_url = os.environ.get('return_url'),
    )
    return redirect(checkout_session.url, code=303)


def buy_order(request):
    '''Покупка и составление заказа заказа'''

    if request.method == 'POST':
        currency = request.POST.get('choise')
        stripe.api_key = settings.STRIPE_TEST_SKEY
        basket = request.session.get('order_list')
        queryset = Item.objects.filter(id__in = basket.keys())
        order =Order()
        order.save()
        list_items = []
        order_details = {}
        for it in queryset:
            if not basket.get(str(it.id)):
                continue
            if it.currency == currency:
                list_items.append(
                    {
                        'price' : it.stripe_price_id,
                        'quantity' : basket.get(str(it.id)),
                    }
                )
                order.item.add(it)
                order_details[it.name] = basket.pop(str(it.id))
        order.order_details = order_details
        checkout_session = stripe.checkout.Session.create(
            line_items = list_items,
            mode = "payment",
            success_url = os.environ.get('success_url'),
            #return_url = os.environ.get('return_url'),
        )
        order.total_price = checkout_session['amount_total']/100
        order.save()
        request.session['order_list'] = basket
        return redirect(checkout_session.url, code=303)

    basket = request.session.get('order_list')
    queryset = Item.objects.filter(id__in = basket.keys())
    currencys = set()
    for it in queryset:
        it_id = str(it.id)
        if not basket.get(it_id) and it_id in basket:
            del basket[it_id]
        currencys.add(it.currency)
    return render(request, 'order.html', {'order': queryset, 'basket' : basket, 'currencys' : currencys})


def watch_items(request):
    '''Страница с товарами'''

    it = Item.objects.all()
    params = {'it' : it}
    basket = request.session.get('order_list')
    if basket:
        params['order'] = sum(basket.values())
    return render(request, 'items.html', params)


def item_id(request, id):
    '''Страница с описанием товара'''

    if not request.session.get('order_list', {}):
        request.session['order_list'] = {}
        request.session.modified = True
    this_item = Item.objects.get(id = id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = int(form.cleaned_data['quantity'])
            request.session['order_list'][str(id)] = quantity
    return render(request, 'this_item.html', {'this_item': this_item, 'form' : OrderForm(), 'quantity' : request.session['order_list'].get(str(id))})


def payment_successful(request):
    '''Успешный URL'''

    return render(request, 'payment.html', {'payment' : 'successful'})
        

def payment_cancelled(request):
	return render(request, 'payment.html', {'payment' : 'cancelled'})
