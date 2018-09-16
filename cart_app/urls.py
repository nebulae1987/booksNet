from django.urls import path
from . import views

urlpatterns = [
    #购物车页面：
    path('cartPage/', views.cartPage,name= 'cartPage'),
    # #展示购物车：
    # path('showCart/', views.showCart,name= 'showCart'),

    #添加购物车：
    path('addCart/', views.addCart,name= 'addCart'),
    #删除购物车
    path('delCart/', views.delCart,name= 'delCart'),
    #修改购物车商品数量
    path('changeCart/', views.changeCart,name= 'changeCart'),
    #恢复删除：
    path('back_del/', views.back_del,name= 'back_del'),


]