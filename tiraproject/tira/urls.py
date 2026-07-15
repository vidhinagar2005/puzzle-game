from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home,name='home'),
    # path('makeup/',views.makeup, name='makeup'),
    path('category/<str:name>', views.category, name='category2'),
    path('singal_product/<int:product_id>', views.singal_product, name='singal_product'),
    path('add_to_cart/<int:product_id>',views.add_to_cart, name='add_to_cart'),
    path('cart_view',views.cart_view, name='cart_view'),
    path('register',views.register, name='register'),
    path('login', views.login_user, name='login_user'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name="update_cart"),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('account/',views.account,name='account'),
    path('logout', views.logout_user, name='logout_user'),
    path('add_to_wishlist/<int:product_id>', views.add_to_wishlist, name="add_to_wishlist"),
    path('wishlist_view/', views.wishlist_view, name='wishlist_view'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name="remove_from_wishlist"),
    # path("initiate/", views.initiate_payment, name="initiate_payment"),
    # path("callback/", views.payment_callback, name="payment_callback")/
    # path('create_order/', views.create_order, name='create_order'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name="update_cart"),
    path('create-order/', views.create_order, name='create_order'),

]