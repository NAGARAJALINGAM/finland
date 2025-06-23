from django.shortcuts import render
from users.models import CustomUser
from django.db.models import Count, Q, Max, Min
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from adminapp .models import Rolemaster,RoleMapping
import json
from django.db import transaction
from users.get_role_details import get_user_roles
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
        if access_roles not in ['superadmin']:
            return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        if Rolemaster.objects.filter(role=role_name).exists():
            return Response({'status': 'warning', 'message': 'Role name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transaction.set_autocommit(False)

            roleobj = Rolemaster(role=role_name,role_desc=role_description,created_by=request.user.id)
            roleobj.save()
            transaction.commit()
            message = 'Rolemaster created successfully'
            return Response({'status': 'success', 'message': message}, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.rollback()
            return Response({'status': 'error', 'message': 'Something went wrong...' + str(e)},status=status.HTTP_400_BAD_REQUEST)




