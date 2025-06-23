from django.urls import path,include
from users import views

app_name = 'users'

urlpatterns = [

    path('create/users/', views.Useronboarding.as_view(), name='user_onboarding'),
    path('login/',views.LoginAPI, name='login'),
    path('forgot_password/',views.ForgotpasswordAPI, name='forgot_password_api'),

]