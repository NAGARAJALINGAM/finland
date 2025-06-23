from django.shortcuts import render
from users.models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Count, Q, Max, Min
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from adminapp .models import Rolemaster,RoleMapping
from rest_framework import status
import json
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from datetime import date,datetime
import random
from users.auth import email_validations
from django.contrib.auth.hashers import make_password,check_password
from users.get_role_details import get_user_roles
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

@api_view(['POST'])
@permission_classes([AllowAny, ])
def LoginAPI(request):
    if request.method == 'POST':
        data=request.data
        mobile_num = data.get('mobile_number')
        password = data.get('password')

        try:
            userobj =  CustomUser.objects.get(mobilenumber=mobile_num)
        except CustomUser.DoesNotExist():
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
            details=[]
            details.append({
                "firstname":userobj.first_name,
                "lastname":userobj.last_name,
                "role":authorized_roles,
                "token":token
            })
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

