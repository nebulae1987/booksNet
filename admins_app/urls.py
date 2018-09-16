from django.urls import path
from . import views

urlpatterns = [
    #管理后台页面：
    path('adminsIndex/', views.adminsIndex,name= 'adminsIndex'),
    #添加图书展示列表等页面：
    path('add/', views.add,name= 'add'),
    path('dzlist/', views.dzlist,name= 'dzlist'),
    path('list/', views.list,name= 'list'),
    path('splb/', views.splb,name= 'splb'),
    path('zjsp/', views.zjsp,name= 'zjsp'),
    path('zjzlb/', views.zjzlb,name= 'zjzlb'),
    #删除书籍
    path('del_book/', views.del_book,name= 'del_book'),
    #修改书籍
    path('reviseBook/', views.reviseBook,name= 'reviseBook'),
    path('reviseLogic/', views.reviseLogic,name= 'reviseLogic'),
    #添加一级二级分类
    path('add_a/', views.add_a,name= 'add_a'),
    path('add_b/', views.add_b,name= 'add_b'),


]