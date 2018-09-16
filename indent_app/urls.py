from django.urls import path
from . import views

urlpatterns = [
    #订单页面：
    path('indentPage/', views.indentPage,name= 'indentPage'),
    path('indentLogic/', views.indentLogic,name= 'indentLogic'),
    #订单确认页
    path('indentConfirm/', views.indentConfirm,name= 'indentConfirm'),
    #订单完成页
    path('indentOk/', views.indentOk,name= 'indentOk'),
    path('indentOkPage/', views.indentOkPage,name= 'indentOkPage'),
    #用户选择地址项
    path('se_addr/', views.se_addr,name= 'se_addr'),


]