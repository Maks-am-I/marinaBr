from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_item_view, name='update_cart_item'),
    path('cart/add-solution/<int:solution_id>/', views.add_ready_solution_to_cart_view, name='add_ready_solution_to_cart'),
    path('cart/remove-solution/<int:solution_id>/', views.remove_ready_solution_from_cart_view, name='remove_ready_solution_from_cart'),
    path('cart/update-solution/<int:solution_id>/', views.update_ready_solution_cart_item_view, name='update_ready_solution_cart_item'),
    path('cart/info/', views.get_cart_info, name='cart_info'),
    path('cart/order/', views.create_order, name='create_order'),
]