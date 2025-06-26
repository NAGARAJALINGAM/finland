from django.shortcuts import render
from users.models import CustomUser
from django.db.models import Count, Q, Max, Min
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from adminapp .models import Rolemaster,RoleMapping,Productmaster,Cartitems,OrderDetails,SellableOrderDetails
import json
from django.db import transaction
from users.get_role_details import get_user_roles
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from adminapp .forms import Productmasterform
from django.contrib.auth.decorators import login_required

class RoleMasterAPI(APIView):

    def get(self,request):
        data=request.query_params
        roleid=data.get('roleid')
        role_name = []
        if role_name in ['admin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        if roleid is not None:
            roleobj = [Rolemaster.objects.filter(id=roleid)]
        else:
            roleobj = Rolemaster.objects.filter(is_active=True)
        try:
            details = []
            for obj in roleobj:
                details.append({
                    "rolename":obj.role,
                    "description":obj.role_desc,
                })
            message = 'Role details fetched successfully'
            return Response({'status': 'success', 'message': message,'data':details}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):
        data=request.data
        role_name = data.get("role_name")
        role_description = data.get("description")
        access_roles = get_user_roles(request)
        if access_roles not in ['superadmin','admin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        if Rolemaster.objects.filter(role=role_name).exists():
            return Response({'status': 'warning', 'message': 'Role name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transaction.set_autocommit(False)
            created_by='2'
            roleobj = Rolemaster(role=role_name,role_desc=role_description,created_by=int(created_by))
            roleobj.save()
            transaction.commit()
            message = 'Rolemaster created successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.rollback()
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)

def product_list_page(request):
    return render(request, 'adminapp/product_list.html')


def product_create_page(request):
    return render(request, 'adminapp/product_create.html')

class ProductmasterAPI(APIView):

    def get(self,request):
        data=request.query_params
        productid = data.get('productid',None)

        access_role=get_user_roles(request)
        if access_role not in ['admin','user']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        if productid is not None:
            product_obj = [Productmaster.objects.get(id=productid)]
        else:
            product_obj = Productmaster.objects.filter(is_active=True)

        try:
            details=[]
            for obj in product_obj:
                details.append({
                    "id":obj.id,
                    "product_name":obj.product,
                    "is_active":obj.is_active,
                    "is_return_p    licy_available":obj.is_return_policy_available,
                    "return_policy":obj.return_policy,
                    "product_stock":obj.product_stock
                })
            message = 'products fetched successfully'
            return Response({'status': 'success', 'message': message,'data':details}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data=request.data
        product = data.get('product')
        description = data.get('description',None)
        product_stock = data.get('product_stock','10')
        images = data.get('images',[])
        expected_delivery_days = data.get('expected_delivery_days','10')
        return_days = data.get('return_days','0')
        mrp = data.get('mrp')
        print("images==",images)
        access_role=get_user_roles(request)
        print(access_role)
        if access_role not in ['admin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if Productmaster.objects.filter(product__iexact=product).exists():
            return Response({'status': 'warning', 'message': 'Product name already exists'}, status=status.HTTP_400_BAD_REQUEST)
       
        transaction.set_autocommit(False)
        try:
            print(request.user)
            createdby=2
            productobj = Productmaster(product=product,description=description,images=images,product_stock=product_stock,
                                       expected_delivery_days=expected_delivery_days,return_days=return_days,created_by=int(createdby),mrp=mrp)
            productobj.save()
            transaction.commit()
            message = 'products created successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        data=request.data
        productid = data.get('productid')
        product = data.get('product',None)
        description = data.get('description',None)
        product_stock = data.get('product_stock',None)
        images = data.get('images',{})
        expected_delivery_days = data.get('expected_delivery_days')
        return_days = data.get('return_days')
        mrp = data.get('mrp')

        access_role=get_user_roles(request)
        
        if access_role not in ['admin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            productobj=Productmaster.objects.get(id=productid)
        except Productmaster.DoesNotExist:
            return Response({'status': 'warning', 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Productmaster.objects.filter(product__iexact=product).exclude(id=productid).exists():
            return Response({'status': 'warning', 'message': 'Product name already exists'}, status=status.HTTP_400_BAD_REQUEST)


        transaction.set_autocommit(False)
        try:
            productobj.product=product
            productobj.description=description
            productobj.product_stock=product_stock if product_stock is not None else productobj.product_stock
            productobj.return_days=return_days if return_days is not None else productobj.return_days
            productobj.expected_delivery_days=expected_delivery_days if expected_delivery_days is not None else productobj.expected_delivery_days
            productobj.images=images
            productobj.modified_by=request.user.id
            productobj.save()
            message = 'products updated successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        data=request.data
        productid = data.get('productid')

        access_role=get_user_roles(request)
        
        if access_role not in ['admin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            productobj=Productmaster.objects.get(id=productid)
        except Productmaster.DoesNotExist:
            return Response({'status': 'warning', 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
       
        transaction.set_autocommit(False)
        try:
            productobj.is_active=False
            productobj.modified_by=request.user.id
            productobj.save()

            message = 'products deleted successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)


def product_creation(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            description = data.get('description',None)
            product_stock = data.get('product_stock','10')
            images = data.get('images',{})
            expected_delivery_days = data.get('expected_delivery_days','10')
            return_days = data.get('return_days','0')


            productobj = Productmaster.objects.create(name=name,description=description,product_stock=product_stock,
                                                   images=images,expected_delivery_days=expected_delivery_days,
                                                   return_days=return_days,created_by=request.user.id)

            if request.is_ajax():
                return JsonResponse({
                    "success": True,
                    "message": f"{productobj.name} added."
                })
            else:
                return redirect("/template/productdetails.html/")
        else:
            form = Productmasterform()

        return render(request, 'home/workout_schedule.html', {'form': form, 'form_new': form_new, 'exercise_form': exercise_form})
    except Exception as e:
        print("err=", e)
        return JsonResponse({
            "success": False,
            "message": "An error occurred while processing the request."
        }, status=500)

def product_list_create(request):
    if request.method == 'POST':
        form = Productmasterform(request.POST)
        if form.is_valid():
            productobj=form.save(commit=False)
            productobj.created_by = request.user
            productobj.save()
            return redirect('adminapp:product-list')  #Redirect to the same view
    else:
        form = Productmasterform()
    return render(request, 'adminpp/product_list_create.html', {'form': form})


# def product_list(request):
#     products = Productmaster.objects.all().order_by('-created_at')
#     return render(request, 'adminapp/product_list.html', {'products': products})



class CartItemCrud(APIView):

    def get(self,request):
        data=request.query_params
        productid = data.get('productid')

        access_role=get_user_roles(request)
        if access_role not in ['user']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        if productid is not None:
            cart_product_obj = [Cartitems.objects.get(product_id=productid)]
        else:
            cart_product_obj = Cartitems.objects.filter(is_active=True)

        try:
            details=[]
            for obj in cart_product_obj:
                details.append({
                    "cart_id":obj.id,
                    "product_id":obj.product.id,
                    "product_name":obj.product.product,
                    "quantity":obj.quantity,
                    "is_active":obj.is_active,
                    "is_return_policy_available":obj.product.is_return_policy_available,
                    "return_policy":obj.product.return_policy,
                    "product_stock":obj.product.product_stock
                })
            message = 'Cart products fetched successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data=request.data
        product = data.get('product')
        quantity = data.get('quantity')

        access_role=get_user_roles(request)
        print(access_role)
        if access_role !='user':
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this actions'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            productobj = Productmaster.objects.get(id=product)
        except Productmaster.DoesNotExist:
            return Response({'status': 'warning', 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.set_autocommit(False)
        created_by='3'
        try:
            cartitem_obj = Cartitems.objects.get(user_id=11,product=productobj)
            cartitem_obj.quantity=quantity
            cartitem_obj.save()
        except Cartitems.DoesNotExist:    
            cartitem_obj=Cartitems(
                user_id = 3,
                product = productobj,
                quantity = quantity,
                created_by = created_by,
            )
            cartitem_obj.save()
            transaction.commit()
            message = 'cart items created successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        data=request.data
        cartid = data.get('cartid')
        product = data.get('product')
        quantity = data.get('quantity')

        access_role=get_user_roles(request)
        
        if access_role not in ['user']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            cart_product_obj=Cartitems.objects.get(id=cartid)
        except Cartitems.DoesNotExist:
            return Response({'status': 'warning', 'message': 'cart not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction.set_autocommit(False)
            cart_product_obj.product=product
            cart_product_obj.quantity=quantity
            cart_product_obj.modified_by=request.user.id
            cart_product_obj.save()
            transaction.commit()
            message = 'cart products updated successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)