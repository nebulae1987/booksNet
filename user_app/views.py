import hashlib,random
import string
from captcha.image import ImageCaptcha
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user_app.models import User

# Create your views here.
#密码加密
def makepwd(pwd,salt=None):
    print('this is make the password')
    h = hashlib.md5()
    if not salt:
        # 无salt时为注册过程：
        abc = '123456789!@#$%^&*()_+abcdefghijklmnopsrstuvwxyz~/.,|><'
        salt = ''.join(random.sample(abc,10)).replace(' ','')
        pwd = pwd+salt
        h.update( pwd.encode())
        mypwd = h.hexdigest()
        #得到最终随机码+用户输入密码的hash码密码，返回hash密码和salt保存到用户表
        return mypwd,salt
    else:
        #有salt,此时是登录过程：根据账户查数据库salt，并与输入密码传入此处处理，返回最终mypwd的hash密码
        pwd = pwd + salt
        h.update(pwd.encode())
        mypwd = h.hexdigest()
        return mypwd

#登录页面
def loginpage(request):
    print('this is loginpage')
    return render(request,'booksNet/user/login.html')
def login_logic(request):
    print('this is login_logic')
    # flag = request.POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    autologin = request.POST.get('autologin')
    print('name+pwd:',username,password,'autologin:',autologin)
    #如果用户勾选记住密码：
    salt = User.objects.filter(username=username)
    print('salt:',salt)
    if salt:
        salt = salt[0].salt
        password = makepwd(password,salt)
        login = User.objects.filter(username=username,password=password)[0]
        print('password:',password)
        if login:
            request.session['login_user']=username
            if request.session.get('login_flag') == 'indent':
                #响应2表示跳转到订单页面
                del request.session['login_flag']
                return HttpResponse('2')
            else:
                return HttpResponse('1')
    else:
        return HttpResponse('0')

#注册页面
def registpage(request):
    print('this is registpage')
    return render(request,'booksNet/user/register.html')
#注册成功页面
def registok(request):
    print('this is registok')
    username = request.session.get('login_user')
    return render(request,'booksNet/user/register ok.html',{'username':username})
#注册逻辑：
def regist_logic(request):
    print('this is regist_logic')
    #尝试获得用户跳转来的位置标志
    flag = request.POST.get('flag')
    username = request.POST.get('txt_username')
    password = request.POST.get('txt_password')
    repassword = request.POST.get('txt_repassword')
    vcode = request.POST.get('txt_vcode')
    mycode = request.session.get('mycode')
    if password == repassword :
        #调用函数获得加密密码和salt
        result = makepwd(password)
        password = result[0]
        salt = result[1]
        user = User.objects.create(username=username,password=password,salt = salt)
        #登录成功后创建保持用户登录状态的session
        request.session['login_user'] = username
        return HttpResponse('1')
    else:
        return HttpResponse('0')

#生成验证码
def getcode(request):
    print('this is makecode logic')
    strcode = ''.join(random.sample(string.ascii_letters+string.digits,4))
    img = ImageCaptcha()
    mycode = img.generate(strcode)
    request.session['mycode'] = strcode
    print(strcode)
    return HttpResponse(mycode,'image/png')

#异步验证注册账号是否可用
def check_username(request):
    print('this is check username')
    username = request.GET.get('username')
    print('username:', username)
    data_name = User.objects.filter(username=username)
    print('data_name:', data_name)
    if data_name:

        return HttpResponse('1')
    else:
        return HttpResponse('0')

#验证验证码是否正确
def checkcode(request):
    print('this is check code')
    code = request.GET.get('code')
    mycode = request.session.get('mycode')
    print('mycode:',mycode,'usercode:',code)
    if code.lower() == mycode.lower():
        return HttpResponse('1')
    else:
        return HttpResponse('0')
#登出：
def log_out(request):
    print('this is logout ')
    log = request.GET.get('log')
    if request.session.get('login_user') and log == '1':
        del request.session['login_user']
        return HttpResponse('1')
    return HttpResponse('0')

