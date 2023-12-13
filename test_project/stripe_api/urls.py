from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.buy_id, name = 'buy_priduct'),
    path('order/', views.buy_order, name = 'buy_order'),
    path('item/', views.watch_items, name = 'watch_priducts'),
    path('item/<int:id>/', views.item_id, name = 'watch_priduct'),
    path('payment_successful', views.payment_successful, name = 'payment_successful'),
    path('payment_cancelled', views.payment_cancelled, name = 'payment_cancelled'),
]