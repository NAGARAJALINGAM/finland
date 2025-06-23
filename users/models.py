from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

# class customuserbase(AbstractBaseUser):
#     def create_user(self,mobilenumber,password=None,**extra_fields):
#         if not mobilenumber:
#             return ValueError("mobilenumber is required")
#         user = self.model(mobilenumber=mobilenumber,**extra_fields)
#         user = set_password(password)
#         user.save()
   
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=55,null=True,blank=True)
    mobilenumber = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)     
    modified_by = models.CharField(max_length=20,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_regular_customer = models.BooleanField(default=False)
    tempcode = models.CharField(max_length=50, blank=True, null=True)
    native = models.CharField(max_length=100,blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)    
    emergency_contactno = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    country_id = models.CharField(max_length=10,null=True,blank=True)
    profilephoto = JSONField(blank=True, default=dict)
    coverphoto = JSONField(blank=True, default=dict)
    is_seller = models.BooleanField(default=False)

    class Meta:
        db_table = ("users")
        ordering = ('-created_at',)
