from django.urls import path,include
from adminapp import views
from django.contrib.auth import views as auth_views

app_name = 'adminapp'

urlpatterns = [

    path('create/role/', views.RoleMasterAPI.as_view(), name='create_role'),
    path('products/', views.product_list_page, name='product-list-page'),
    path('products/new/', views.product_create_page, name='product-create-page'),

    path('create/products/', views.ProductmasterAPI.as_view(), name='create_products'),
    path('cart/creation/', views.CartItemCrud.as_view(), name='cart_creation'),

    # path('products/', views.product_list_create, name='product-create'),
    # path('products/list/', views.product_list, name='product-list'),  # 👈 new list page
    
]