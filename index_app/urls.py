from django.urls import path
from . import views

urlpatterns = [
    #首页展示：
    path('indexpage/', views.index_page,name= 'index_page'),
    #添加图书：
    path('addpage/', views.addpage,name= 'addpage'),
    path('addbook/', views.addbook,name= 'addbook'),
    #图书详情页：
    path('bookpage/',views.book_page, name = 'bookpage'),
    #图书分类页：
    path('booklist/',views.booklist, name = 'booklist'),

]
