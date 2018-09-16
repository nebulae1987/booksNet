from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from index_app.models import Book, Category


#首页页面:
def index_page(request):
    print('this is index_page')
    #分类对象：
    a = Category.objects.filter(category_p=0)
    b = Category.objects.exclude(category_p=0)
    #获取登录成功的用户
    username = request.session.get('login_user')
    #图书对象，编辑推荐0-24控制8*3页，新书推荐按上线时间倒序排列8*3页，侧栏热销新书榜倒序排序10本：
    editor_book = Book.objects.all().order_by('-editor_recommend')[0:24]
    new_book = Book.objects.all().order_by('-online_date')[0:24]
    new_hot_book = Book.objects.all().order_by('-sales','-online_date')[0:10]
    return render(request, 'booksNet/index.html',{'editor_book':editor_book,'new_book':new_book,'new_hot_book':new_hot_book,'a':a,'b':b,'username':username})

#图书详情页：
def book_page(request):
    print('this is book_page')
    #获取请求查看的图书id
    book_id = request.GET.get('id')
    #判断登录状态：
    username = request.session.get('login_user')
    #未点击跳转进页面的链接默认查看id=10的book
    if not book_id:
        book_id = 10
    book = Book.objects.get(pk=book_id)
    return render(request,'booksNet/book/Book details.html',{'book':book,'username':username})

#图书列表页：
def booklist(request):
    print('this is booklist page')
    # 判断登录状态：
    username = request.session.get('login_user')
    # 为页面左侧栏一二级分类展示获取分类表中所有一二级对象：
    a = Category.objects.filter(category_p=0)
    b = Category.objects.exclude(category_p=0)
    #获取分类参数a一级分类b二级分类：
    alevel = request.GET.get('a')
    blevel = request.GET.get('b')
    #获取请求分页数
    num = request.GET.get('num')
    #判断有请求参数且不是None时转换为int型
    if blevel and blevel !='None':
        blevel = int(blevel)
    if alevel and alevel !='None':
        alevel = int(alevel)
    if num and num != 'None':
        num = int(num)
    # 如果只点击一级分类：
    if  not blevel or blevel=='None':
        l_book = []
        cate = Category.objects.filter(category_p=alevel)
        #如果点击的一级分类有二级分类，则通过一级分类找到所有二级分类，再通过所有二级分类遍历查找所有对应图书
        if cate:
            for i in cate:
                for j in i.book_set.all():
                    l_book.append(j)
            books = l_book
        else:
            #如果点击的一级分类没有二级分类，则直接在图书表查询其直接分类编号
            books = Book.objects.filter(category_id=alevel)
    else:
        #通过二级分类查二级分类下所有图书
        abooks = Category.objects.get(pk=blevel)
        books = abooks.book_set.all()
    # 对查询到的图书分页：
    if not num:
        num = 1
    else:
        num = int(num)
    pagtor = Paginator(books,per_page=4)
    books = pagtor.page(number=num)
    return render(request, 'booksNet/book/booklist.html', {'books': books,'aid':alevel,'bid':blevel,'a':a,'b':b,'username':username})


#简陋的添加书籍页面：
def addpage(request):
    print('this is addbook page')
    return render(request,'test/uploadbook.html')
#添加书籍逻辑
def addbook(request):
    print('this is add book,uploadbook!')
    try:
        with transaction.atomic():
            name = request.POST.get('name')
            author = request.POST.get('author')
            pub_company = request.POST.get('pub_company')
            pub_time = request.POST.get('pub_time')
            revision = request.POST.get('revision')
            ISBN   = request.POST.get('ISBN')
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

            if not editor_recommend:
                editor_recommend = None
            book = Book(name = name,author=author,pub_company=pub_company,pub_time=pub_time,revision=revision,ISBN=ISBN, word_count=word_count,page_count=page_count,page_type=page_type,paper=paper,wrapper=wrapper,dprice=dprice, price=price,editor_recommend=editor_recommend,digest_img=digest_img,book_img=book_img, print_time=print_time,impression=impression,stock=stock,online_date=online_date,score=score,sales=sales,category_id=category_id)
            book.save()
            return redirect('admins:list')
    except:
        return  HttpResponse('add failed!')
