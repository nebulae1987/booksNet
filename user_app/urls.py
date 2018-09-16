from django.urls import path
from . import views

urlpatterns = [
    #登录页面：
    path('loginpage/', views.loginpage,name= 'loginpage'),
    path('login_logic/', views.login_logic,name= 'login_logic'),
    #注册页面：
    path('registpage/', views.registpage,name= 'registpage'),
    #注册成功页面：
    path('registok/', views.registok,name= 'registok'),
    #注册逻辑
    path('regist_logic/', views.regist_logic,name= 'regist_logic'),

    #生成验证码
    path('getcode/',views.getcode,name = 'getcode'),
    #校验验证码
    path('checkcode/',views.checkcode,name = 'checkcode'),

    #验证用户名是否可用：
    path('check_username/',views.check_username,name='check_username'),
    #登出：
    path('log_out/',views.log_out,name = 'log_out'),
]