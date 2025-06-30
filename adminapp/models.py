from django.db import models
from users.models import CustomUser
# Create your models here.
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
# 
def product_image_upload_path(instance, filename):
    return f'products/{instance.product}/{filename}'
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
    product_image = models.ImageField(upload_to=product_image_upload_path,blank=True,null=True)
    mrp = models.DecimalField(max_digits=29, decimal_places=3, default='0')
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = ("product_master")
        ordering = ('created_at',)


class OrderDetails(models.Model):

    """This is the model to save the order details"""

    consumerid = models.CharField(max_length=32, blank=True, null=True)
    product_id = models.ForeignKey(Productmaster, on_delete=models.SET_NULL, null=True, related_name='productid')
    completeddatetime = models.DateTimeField(null=True)
    cancellationdone = models.BooleanField(default=False)
    cancelled_by = models.CharField(max_length=30, blank=True, null=True)
    cancellationdatetime = models.DateTimeField(null=True)
    paymentdone = models.BooleanField(default=False)
    order_status = models.CharField(max_length=32, default='inprogress')
    wrapupsstatus = models.CharField(max_length=32, default='')
    order_completed = models.BooleanField(default=False)
    created_by = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    cancellationreason = models.CharField(max_length=300, null=True)
    class Meta:
        db_table = 'order_details'
        ordering = ('-created_at',)

class Cartitems(models.Model):

    product=models.ForeignKey(Productmaster,on_delete=models.CASCADE,related_name = 'cartitem_user_product')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name = 'cartitem_user')
    quantity=models.IntegerField(default=0)  
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = ("user_cart")
        ordering = ('-created_at',)


class SellableOrderDetails(models.Model):
    #store the user where user is in CustomUser
    orderid = models.ForeignKey(OrderDetails, related_name='orderdetails_id', on_delete=models.CASCADE)
    item_count=models.IntegerField(blank=True,null=True,default=0)
    price=models.DecimalField(max_digits=10,default=0,decimal_places=3)
    total_tax=models.DecimalField(max_digits=10,default=0,decimal_places=3)
    total_price=models.DecimalField(max_digits=10,default=0,decimal_places=3)
    total_delivery_fee = models.DecimalField(max_digits=19, decimal_places=3, default='0')
    is_returned=models.BooleanField(default=False)
    return_replace_actiondetails = JSONField(default=dict,null=True,blank=True)
    return_pickup_location=models.CharField( max_length=250,null=True, blank=True)
    return_reason=models.TextField(blank=True,null=True)
    return_quantity=models.IntegerField(default=0)
    return_price=models.DecimalField(max_digits=10,default=0,decimal_places=3)
    return_tax_total=models.DecimalField(max_digits=10,default=0,decimal_places=3)
    return_price_total=models.DecimalField(max_digits=10,default=0,decimal_places=3)
    approved_by=models.IntegerField(blank=True, null=True)
    return_completed_time=models.DateTimeField(null=True, blank=True)
    is_replacement=models.BooleanField(default=False)
    replacement_pickup_location=models.CharField( max_length=250,null=True, blank=True)
    replacement_reason=models.TextField(blank=True,null=True)
    replacement_completed_time=models.DateTimeField(null=True, blank=True)
    return_replace_quantity=models.IntegerField(default=0)
    delivered_location= models.TextField(null=True, blank=True)
    delivered_area = models.CharField(max_length=30,null=True,blank=True)
    delivered_time=models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)  
    modified_by = models.IntegerField(blank=True, null=True)   
   
    class Meta:
        db_table = 'sellable_order_details'
        ordering = ('created_at',)
 