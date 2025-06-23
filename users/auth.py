import re
from datetime import datetime
import calendar
from calendar import monthrange
from .models import CustomUser
from django.core.validators import validate_email

def email_validations(email):
    
	try:
		validate_email(email)
		return True
	except:
		return False