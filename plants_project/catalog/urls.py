from django.urls import path

from .views import (
    PlantList,
    CartList, CartDelete, CartCheckout,
    OrderList, OrderDetail,PlantDetail, CategoryDetail, CategoryList
)

urlpatterns = [
    path('plants/', PlantList.as_view()),
    path('plants/<int:pk>/', PlantDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    path('cart/', CartList.as_view()),
    path('cart/<int:item_id>/', CartDelete.as_view()),
    path('cart/checkout/', CartCheckout.as_view()),
    path('orders/', OrderList.as_view()),
    path('orders/<int:order_id>/', OrderDetail.as_view()),
]
