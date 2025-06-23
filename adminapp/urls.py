from django.urls import path,include
from adminapp import views

app_name = 'adminapp'

urlpatterns = [

    path('create/role/', views.RoleMasterAPI.as_view(), name='create_role'),

    # path('create/products/', views.Productmaster.as_view(), name='create_products'),

]