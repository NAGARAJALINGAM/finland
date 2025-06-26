from django.urls import path,include
from users import views
from django.views.generic import TemplateView

app_name = 'users'

urlpatterns = [

    path('create/users/', views.Useronboarding.as_view(), name='user_onboarding'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('login_user/',views.LoginAPI, name='login_user'),
    path('forgot_password/',views.ForgotpasswordAPI, name='forgot_password_api'),
    path('create_order/',views.OrderDetailsCreation, name='create_order'),

]