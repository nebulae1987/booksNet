from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from bookcart import Cart
from indent_app.models import Address, Order, ItemOrder
import uuid

from index_app.models import Book
from user_app.models import User
from datetime import datetime

#订单确认页：
def indentConfirm(request):
    print('this is indent confirm')
    username = request.session.get('login_user')
    cart = request.session.get('cart')

    # 根据请求的图书id及其数量添加到购物车
    book_id = request.GET.get('book_id')
    if book_id:
        book_id = int(book_id)
        book_amount = request.GET.get('book_amount')
        print('book_amount',book_amount,book_id)
        book = Book.objects.get(pk=book_id)
        # 如果有数量则添加指定数量书籍，无数量则默认添加一个本
        if book_amount:
            book_amount = int(book_amount)
        elif not book_amount or book_amount == 'None':
            book_amount = 1
        # 判断该书库存，若有则添加到session购物车中
        if book.stock >= book_amount:
            cart = request.session.get('cart')
            # 判断是否已有购物车，有则添加书籍，无则创建：
            if cart:
                cart.addCart(book_id, book_amount)
                request.session['cart'] = cart
            else:
                cart = Cart()
                cart.addCart(book_id, book_amount)
                request.session['cart'] = cart

    if cart:
        books = cart.carItem
        if books:
            return render(request,'booksNet/indent/indent_confirm.html',{'books':books,'cart':cart,'username':username})
        return redirect('cart:cartPage')
    else:
        return redirect('cart:cartPage')
#订单确认后生成订单表：
def indentLogic(request):
    print('this is indent logic')
    cart = request.session.get('cart')
    username = request.session.get('login_user')
    try:
        with transaction.atomic():
            if username:
                user = User.objects.get(username = username)
                order_num = str(uuid.uuid4())
                create_date = datetime.now()
                if cart:
                    price = cart.total_price
                    #保存用户订单
                    myorder = user.order_set.create(price = price,order_num=order_num,create_date = create_date,order_user_id=user.id)
                    #保存最近一次订单到session
                    request.session['order_id'] = myorder.id
                    return redirect('indent:indentPage')
            else:
                #确认订单未登录时创建login_flag为订单：indent
                request.session['login_flag'] = 'indent'
                return redirect('user:loginpage')
    except:
        return HttpResponse('生成订单失败，请重试！')
#订单页面：
def indentPage(request):
    print('this is indent page')
    username = request.session.get('login_user')
    #先查询用户是否选择已保存的地址，如果有则显示出来：
    user = User.objects.get(username=username)
    user_addr = user.address_set.all()
    #查询是否有被删除的购物车cart2,有则提取显示供用户选择恢复
    cart2 = request.session.get('cart2')
    cart = request.session.get('cart')
    #通过订单获取总商品数：
    book_amount = 0
    for i in cart.carItem:
        book_amount += i.amount
    if cart2:
        books = cart2.carItem
        if books:
            return render(request,'booksNet/indent/indent.html',{'books':books,'cart2':cart2,'username':username,'total_price':cart.total_price,'book_amount':book_amount,'user_addr':user_addr})
        return render(request, 'booksNet/indent/indent.html',
                      {'username': username, 'total_price': cart.total_price, 'book_amount': book_amount,
                       'user_addr': user_addr})
    else:
        return render(request, 'booksNet/indent/indent.html', {'username': username,'total_price':cart.total_price,'book_amount':book_amount,'user_addr':user_addr})

#订单完成：提交订单后保存根据用户保存其地址：
def indentOk(request):
    print('this is indent ok page')
    #接收用户地址信息保存
    name = request.POST.get('username')
    #为订单完成页传递用户送货用户名
    request.session['addr_user'] = name
    addr = request.POST.get('addr')
    zipcode = request.POST.get('zipcode')
    telphone = request.POST.get('telphone')
    phone = request.POST.get('phone')
    province = request.POST.get('province')
    zone = request.POST.get('zone')
    order_id = request.session.get('order_id')
    # 获取隐藏域：
    book_amount = request.POST.get('book_amount')
    total_price = request.POST.get('total_price')
    print('province:', province,type(province) ,order_id)
    #通过用户存地址表：
    username = request.session.get('login_user')
    user = User.objects.get(username=username)
    try:
        with transaction.atomic():
            #如果用户选择了新建
            if province == '0':
                useraddr = user.address_set.create(name=name,addr=addr,zipcode=zipcode,zone=zone,telphone=telphone,phone=phone)
                #保存地址后把地址id保存到对应的订单表的地址id列：
                useraddrid = Order.objects.get(pk = order_id)
                useraddrid.order_addr_id_id = useraddr.id
                useraddrid.save()
                #存完地址和订单再保存订单项表：order_id,book_amount,total_price
            ItemOrder.objects.create(order_id = order_id,book_amount=book_amount,total_price=total_price)
            # 提交订单完成后删除购物车：
            del request.session['cart']
            return redirect('indent:indentOkPage')
    except:
        return HttpResponse('提交订单失败，请重试！')
#订单完毕页
def indentOkPage(request):
    print('this is indent ok page')
    addr_user = request.session.get('addr_user')
    order_id = request.session.get('order_id')
    order = Order.objects.get(pk = order_id)
    item = ItemOrder.objects.get(order_id=order_id)
    order_price = item.total_price
    book_amount = item.book_amount
    return render(request,'booksNet/indent/indent ok.html',{'order_num':order.order_num,'price':order_price,'book_amount':book_amount,'addr_user':addr_user})

#返回选择的地址：
def se_addr(request):
    print('this is select addr')
    addr_id = request.GET.get('addr_id')
    if addr_id != '0':
        addr_id = int(addr_id)
    else:
        return HttpResponse('0')
    user_addr = list(Address.objects.filter(pk = addr_id).values())
    return JsonResponse(user_addr,safe=False)

#展示订单列表：
def indent_list(request):
    print('this is indent list page')
    orders = Order.objects.all()
    return render(request,'booksNet/indent/indent_list.html')