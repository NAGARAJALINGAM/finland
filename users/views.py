from django.shortcuts import render
from users.models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Count, Q, Max, Min
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from adminapp .models import Rolemaster,RoleMapping,OrderDetails,Productmaster,SellableOrderDetails
from rest_framework import status
import json
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from datetime import date,datetime
import random
from users.auth import email_validations
from django.contrib.auth.hashers import make_password,check_password
from users.get_role_details import get_user_roles
from django import forms
from django.contrib.auth import authenticate, login
from django.db import transaction

class Useronboarding(APIView):
    def get(self,request):
        try:
            data = data.get
            user_id=data.get('user_id')

            role=get_role_details(request)
            if role not in ['admin']:
                return Response({'status':'warning','messege':'you are unauthonticated to do this action'},status=status.HTTP_401_UNAUTHORIZED)
            if user_id is not None:
                try:
                    userobj = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    return Response({'status':'error','message':'user not found'},status=status.HTTP_404_NOT_FOUND)
            else:
                userobj = CustomUser.objects.filter(is_active=True)
            details=[]
            for obj in userobj:
                details.append({
                    "userid":obj.id,
                    "firstname":obj.first_name,
                    "last_name":obj.last_name,
                    "native":obj.native,
                    "mobilenumber":obj.mobilenumber,
                    "email":obj.email,
                    "dob":obj.dob
                })
            return Response({"status":"success","messege":"user details fetched successfully",},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status":"error","message":"something went wrong "+str(e)},status=status.HTTP_400_BAD_REQUEST)
  
    def post(self,request):
        try:
            data = request.data
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            mobilenumber = data.get('mobilenumber')
            password = data.get('password')
            email = data.get('email')
            native = data.get('native',None)
            date_of_birth = data.get('date_of_birth',None)
            role_name = data.get('role_id')

            if CustomUser.objects.filter(mobilenumber=mobilenumber).exists():
                return Response({"status":"warning","messege":"User mobilenumber already exists","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
            
            if CustomUser.objects.filter(email=email).exists():
                return Response({"status":"warning","messege":"User email already exists","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                roleobj = Rolemaster.objects.get(id=role_name)
            except Rolemaster.DoesNotExist:
                return Response({'status':'error','message':'roleid not found'},status=status.HTTP_404_NOT_FOUND)  
            if date_of_birth is not None:
                date_of_birth = datetime.strptime(date_of_birth, "%Y/%m/%d").date()
            username = str(first_name) + " " + str(last_name) 

            user_obj = CustomUser(first_name=first_name,last_name=last_name,mobilenumber=mobilenumber,password=make_password(password),
                                email=email,native=native,date_of_birth=date_of_birth,username=username,created_by=request.user.id)
            user_obj.save()
            rolemapping_obj = RoleMapping(role=roleobj,users=user_obj)
            rolemapping_obj.save()

            return Response({"status":"success","messege":"User created successfully","is_valid":False},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":"error","message":"something went wrong "+str(e)},status=status.HTTP_400_BAD_REQUEST)



from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            mobile_number = form.cleaned_data.get("mobile_number")
            password = form.cleaned_data.get("password")

            user = authenticate(request, mobile_number=mobile_number, password=password)
            
            if user is None:
                msg = 'Profile not found'
                return render(request, "home/login.html", {"form": form, "messages": msg})

            try:
                user_group_obj = CustomUser.objects.get(id=user.id)
            except:
                msg = 'Profile not found'
                return render(request, "home/login.html", {"form": form, "messages": msg})

            if user is not None:
                login(request, user)
                return redirect("/templates/productdetails.html/")

            else:
                msg = 'Invalid credentials'
                return render(request, "home/login.html", {"form": form, "messages": msg})
        else:
            print("error in login", form.errors)
            msg = 'Error validating the form'

        form = Productmasterform()
    return render(request, 'adminpp/product_list_create.html', {'form': form})







@api_view(['POST'])
@permission_classes([AllowAny, ])
def LoginAPI(request):
    if request.method == 'POST':
        data=request.data
        mobile_num = data.get('mobile_number')
        password = data.get('password')

        try:
            userobj =  CustomUser.objects.get(mobilenumber=mobile_num)
        except CustomUser.DoesNotExist:
            return Response ({"status":"warning","messege":"User not found","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
        
        if not check_password(password,userobj.password):
            return Response ({"status":"warning","messege":"Password was wrong","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
        
        if not userobj.is_active:
            return Response ({"status":"warning","messege":"Your account is currently deactivated contact admin for activate","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
        try:
            authorized_roles = RoleMapping.objects.get(users=userobj).role.role
            payload = jwt_payload_handler(userobj)
            payload['role']=authorized_roles                      #including role in this payload
            token = jwt_encode_handler(payload)
            details=[{
                "firstname":userobj.first_name,
                "lastname":userobj.last_name,
                "role":authorized_roles,
                "token":token
            }]
            return Response({"status":"success","messege":"user details fetched successfully","data":details},status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback_info = traceback.format_exc()
            print(f"Traceback: {traceback_info}")
            return Response({"status":"error","message":"something went wrong "+str(e)},status=status.HTTP_400_BAD_REQUEST)

class ForgotpasswordAPI(APIView):
    def put(self,request):
        data=request.data
        email = data.get['email']
        code = random.randrange(100000,999999)

       
        email_check = email_validations(email)
        if not email_check:
            return Response ({"status":"warning","messege":"email was wrong","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
        try:
            if email_check:
                try:
                    userobj =  CustomUser.objects.get(email__iexact=email)
                    CustomUser.objects.filter(email__iexact=email,is_active=True).update(tempcode=code)
                except CustomUser.DoesNotExist():
                    return Response ({"status":"warning","messege":"User not found","is_valid":True},status=status.HTTP_401_UNAUTHORIZED)
            sending_emailobj = sending_emailobj(code)
            return Response({"status":"success","messege":"user details fetched successfully","data":details},status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback_info = traceback.format_exc()
            print(f"Traceback: {traceback_info}")
            return Response({"status":"error","message":"something went wrong "+str(e)},status=status.HTTP_400_BAD_REQUEST)



class OrderDetailsCreation(APIView):

    def get(self,request):
        data=request.query_params
        orderid = data.get('orderid')

        access_role=get_user_roles(request)
        if access_role not in ['user']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        if orderid is not None:
            order_obj = [OrderDetails.objects.get(id=orderid)]
        else:
            order_obj = OrderDetails.objects.filter(is_active=True,created_by=request.user.id)

        try:
            details=[]
            for obj in order_obj:
                details.append({
                    "orderid":obj.id,
                    "product_id":obj.product_id.id,
                    "product_name":obj.product_id.product,
                    "quantity":obj.completeddatetime,
                    "is_paymentdone":obj.paymentdone,
                    "order_status":obj.order_status,
                    "order_completed":obj.order_completed,

                })
            message = 'Order details fetched successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data=request.data
        product = data.get('product')
        quantity = data.get('quantity')
        delivery_area = data.get('delivery_area')
        delivery_location = data.get('delivery_location')
        item_count = data.get('item_count')
        total_delivery_fee = data.get('total_delivery_fee')

        access_role=get_user_roles(request)

        if access_role not in ['admin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            productobj = Productmaster.objects.get(id=product)
        except Productmaster.DoesNotExist:
            return Response({'status': 'warning', 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        transaction.set_autocommit(False)
        try:
            orderobj = OrderDetails(product_id=productobj,consumerid=request.user.id,
                                    created_by=request.user.id)
            orderobj.save()
            selling_obj = SellableOrderDetails(orderid=orderobj,item_count=item_count,quantity=quantity,delivery_location=delivery_location,
                                               delivery_area=delivery_area,created_by=request.user.id,total_price=orderobj.product_id.mrp,total_delivery_fee=total_delivery_fee)
            selling_obj.save()
            transaction.commit()
            message = 'cart items created successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        data=request.data
        orderid = data.get('orderid')
        order_status = data.get('order_status')
        quantity = data.get('quantity')

        access_role=get_user_roles(request)
        
        if access_role not in ['user']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            order_obj=OrderDetails.objects.get(id=orderid)
        except OrderDetails.DoesNotExist:
            return Response({'status': 'warning', 'message': 'order not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction.set_autocommit(False)
            order_obj.order_status=order_status
            order_obj.order_completed=True if order_status == 'completed' else False
            order_obj.modified_by=request.user.id
            order_obj.save()
            transaction.commit()
            message = 'Orders updated successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)