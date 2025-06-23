from django.db import models
from users.models import CustomUser
# Create your models here.
from django.contrib.postgres.fields import JSONField,ArrayField


class Rolemaster(models.Model):
    role = models.CharField(max_length=55,null=True,blank=True)
    role_desc = models.CharField(max_length=55,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    modified_by = models.CharField(max_length=20,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = ("role_master")
        ordering = ('created_at',)




class RoleMapping(models.Model):
    role = models.ForeignKey(Rolemaster,on_delete=models.DO_NOTHING)
    users = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='users_role')
    is_active = models.BooleanField(default=True)
    modified_by = models.CharField(max_length=20,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = ("role_mapping")
        ordering = ('created_at',)


# class categorymaster(models.Model):
#     name = models.CharField(max_length=55,null=True,blank=True)
#     role_desc = models.CharField(max_length=55,null=True,blank=True)
#     is_active = models.BooleanField(default=True)
#     modified_by = models.CharField(max_length=20,null=True,blank=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=20,null=True,blank=True)
#     modified_at = models.DateTimeField(auto_now=True)
    

#     class Meta:
#         db_table = ("role_master")
#         ordering = ('created_at',)


class Productmaster(models.Model):
    product = models.CharField(max_length=55,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    can_be_deleted=models.BooleanField(default=True)
    return_policy=models.TextField(null=True,blank=True)
    return_days=models.CharField(default=0,max_length=50)
    expected_delivery_days=models.CharField(default=0,max_length=50)
    is_exchange_policy_available = models.BooleanField(default=True)
    is_return_policy_available = models.BooleanField(default=True)
    is_published=models.BooleanField(default=False)
    product_stock=models.CharField(max_length=20,default='10')
    images=ArrayField(JSONField(), blank=True, default=list)
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = ("product_master")
        ordering = ('created_at',)