from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from indent_app.models import Address
from index_app.models import Book, Category

#管理后台首页
def adminsIndex(request):
    print('this is adminsindex page')
    return render(request,'booksNet/admins/index.html')
#后台添加图书页面
def add(request):
    b_level = Category.objects.exclude(category_p=0)
    return render(request,'booksNet/admins/main/add.html',{'b_level':b_level})
#地址列表页面：
def dzlist(request):
    print('this is address list')
    pagitor = Paginator(Address.objects.all(),8)
    num = request.GET.get('num')
    if not num:
        num = 1
    addr = pagitor.page(number=num)
    return render(request,'booksNet/admins/main/dzlist.html',{'addr':addr})
#图书列表页面
def list(request):
    number = request.GET.get('num')
    pagtor = Paginator(Book.objects.all(),per_page=10)
    if not number:
        number = 1
    books = pagtor.page(number=number)
    return render(request,'booksNet/admins/main/list.html',{'books':books})
#商品类别：
def splb(request):
    #根据category编号0和非0查询出所有一级二级分类对象：
    a_level = Category.objects.filter(category_p=0)
    b_level = Category.objects.exclude(category_p=0)
    l_level = []
    for i in a_level:
        l_level.append(i)
    for j in b_level:
        l_level.append(j)
    patitor = Paginator(l_level,per_page=15)
    num = request.GET.get('num')
    if not num:
        num = 1
    level = patitor.page(number=num)
    return render(request,'booksNet/admins/main/splb.html',{'a':level})

def zjsp(request):
    pass
    return render(request,'booksNet/admins/main/zjsp.html')
#获取所有一级类别对象
def zjzlb(request):
    a_level = Category.objects.filter(category_p=0)
    return render(request,'booksNet/admins/main/zjzlb.html',{'a_level':a_level})

#删除选定书籍：
def del_book(request):
    print('this is del book')
    #获取请求删除的图书列表：
    ids = request.POST.getlist('se_book')
    try:
        with transaction.atomic():
            for i in ids:
                Book.objects.get(pk = int(i)).delete()
            return redirect('admins:list')
    except:
        return HttpResponse('删除失败！请重新再试！')

#添加一级分类：
def add_a(request):
    print('this is add_a logic')
    a_level = request.POST.get('a_level')
    Category.objects.create(category_name=a_level,category_p=0)
    return redirect('admins:zjsp')

#添加二级分类：
def add_b(request):
    print('this is add_b logic')
    a_level = int(request.POST.get('a_level'))
    b_level = request.POST.get('b_level')
    Category.objects.create(category_name=b_level, category_p=a_level)
    return redirect('admins:zjzlb')

#修改图书信息
def reviseBook(request):
    print('this is revise book')
    id = int(request.POST.get('id'))
    name = request.POST.get('name')
    author = request.POST.get('author')
    pub_company = request.POST.get('pub_company')
    pub_time = request.POST.get('pub_time')
    revision = request.POST.get('revision')
    ISBN = request.POST.get('ISBN')
    word_count = request.POST.get('word_count')
    page_count = request.POST.get('page_count')
    page_type = request.POST.get('page_type')
    paper = request.POST.get('paper')
    wrapper = request.POST.get('wrapper')
    dprice = request.POST.get('dprice')
    price = request.POST.get('price')
    editor_recommend = request.POST.get('editor_recommend')
    digest_img = request.FILES.get('digest_img')
    book_img = request.FILES.get('book_img')
    print_time = request.POST.get('print_time')
    impression = request.POST.get('impression')
    stock = request.POST.get('stock')
    online_date = request.POST.get('online_date')
    score = request.POST.get('score')
    sales = request.POST.get('sales')
    category_id = request.POST.get('category')
    #修改图书对象：
    book = Book.objects.get(pk=id)
    book.name = name
    book.author = author
    book.pub_company =pub_company
    book.pub_time =pub_time
    book.revision = revision
    book.ISBN = ISBN
    book.word_count = word_count
    book.page_count = page_count
    book.page_type = page_type
    book.paper = paper
    book.wrapper = wrapper
    book.dprice = dprice
    book.price = price
    book.editor_recommend =editor_recommend
    book.digest_img=digest_img
    book.book_img = book_img
    book.print_time =print_time
    book.impression=impression
    book.stock=stock
    book.online_date=online_date
    book.score=score
    book.sales=sales
    book.category_id=category_id
    book.save()
    return redirect('admins:list')

#修改图书页面：
def reviseLogic(request):
    print('this is revise Logic')
    se_book = request.GET.get('book_id')
    book = Book.objects.get(pk = se_book)
    return render(request, 'booksNet/admins/main/revisebook.html',{'book':book})
