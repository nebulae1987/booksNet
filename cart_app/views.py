from django.http import HttpResponse
from django.shortcuts import render, redirect
from bookcart import CartItem,Cart
from index_app.models import Book
# Create your views here.

#购物车页面
def cartPage(request):
    print('this is shopping cart page')
    cart = request.session.get('cart')
    username = request.session.get('login_user')
    # 判断是否购物车已经创建
    if cart:
        books = cart.carItem
        if books:
            return render(request, 'booksNet/cart/cart.html', {'books': books,'cart':cart,'username':username})
        else:
            return render(request, 'booksNet/cart/cart.html', {'username': username})
    else:
        return render(request, 'booksNet/cart/cart.html',{'username':username})


#添加购物车商品：
def addCart(request):
    print('this is add book to cart')
    #根据请求的图书id及其数量添加到购物车
    book_id = int(request.GET.get('book_id'))
    book_amount = request.GET.get('book_amount')
    book = Book.objects.get(pk = book_id)
    #如果有数量则添加指定数量书籍，无数量则默认添加一个本
    if book_amount:
        book_amount = int(book_amount)
    else:
        book_amount = 1
    #判断该书库存，若有则添加到session购物车中
    if book.stock >= book_amount:
        cart = request.session.get('cart')
        #判断是否已有购物车，有则添加书籍，无则创建：
        if cart:
            cart.addCart(book_id,book_amount)
            request.session['cart'] = cart
        else:
            cart = Cart()
            cart.addCart(book_id,book_amount)
            request.session['cart'] = cart
        #有库存并添加成功返回1
        return HttpResponse('1')
    #没有库存则返回0表示没有库存
    else:
        return HttpResponse('0')

#修改购物车商品：
def changeCart(request):
    print('this is change shopping cart')
    #获取请求要修改的商品id及其数量
    book_id = int(request.GET.get('book_id'))
    book_amount = int(request.GET.get('book_amount'))
    # 判断库存是否有用户需求数量商品,有则添加，无则提示:
    book_stock = Book.objects.get(pk = book_id).stock
    if book_stock >= book_amount:
        cart = request.session.get('cart')
        cart.changeCart(book_id,book_amount)
        request.session['cart'] = cart
        return HttpResponse('1')
    else:
        #如果库存不够
        return HttpResponse('库存不足！')


#删除购物车商品：
def delCart(request):
    print('this is del cart shopping')
    id = request.GET.get('id')
    book_amount = int(request.GET.get('book_amount'))
    #获取请求要删除的商品id及其数量，并创建cart2，以备恢复购物车商品
    cart = request.session.get('cart')
    cart2 = request.session.get('cart2')
    if cart:
        #删除前先添加到新购物车中
        if cart2:
            cart2.addCart(id,book_amount)
            request.session['cart2'] = cart2
        else:
            cart2 = Cart()
            cart2.addCart(id,book_amount)
            request.session['cart2'] = cart2
        #添加到恢复车后再删除购物车中该书籍
        cart.delCart(int(id))
        request.session['cart'] = cart
        return redirect('cart:cartPage')

#恢复删除的商品：
def back_del(request):
    print('this is back del')
    book_id = int(request.GET.get('book_id'))
    book_amount = int(request.GET.get('book_amount'))
    cart2 = request.session.get('cart2')
    book = Book.objects.get(pk=book_id)
    #判断库存,先添加到购物车再删除cart2
    if book.stock:
        cart = request.session.get('cart')
        cart.addCart(book_id,book_amount)
        request.session['cart'] = cart
    if cart2:
        cart2.delCart(book_id)
    return redirect('indent:indentPage')