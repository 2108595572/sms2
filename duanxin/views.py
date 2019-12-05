
from django.shortcuts import render,redirect
from django.http import request
from django.http.response import HttpResponse, JsonResponse
#导入缓存对象
from django.core.cache import cache
from utils import aliyunsms, restful
import json
from .models import *
from utils.restful import result
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from utils.forms import RegisterForm
import logging
# 首页显示验证码
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

def index(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        Reader.objects.create(username=username, password=password, phone=phone, email=email)
        # collect_logger.info("用户：",username)
        return redirect('duanxin:ajax_html')
    #跳转页面时,初始化图文验证码表单项,传递到index页面
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    register_form = RegisterForm()
    return render(request, 'index.html',locals())

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            name = Reader.objects.filter(username=username).values()
            if password == name[0]['password']:
                return redirect('duanxin:books')
            return render(request, 'login.html', {'err': '密码不正确'})
        return render(request, 'login.html', {'err': '请完整输入信息'})
    return render(request, 'login.html')

def books(request):
    # all = Books.objects.all()
    # count_all = (len(list(all)))
    # page = Paginator(all, 2)
    # try:
    #     number = request.GET.get('index', '1')
    #     num = page.page(number)
    # except PageNotAnInteger:
    #     num = page.page(1)
    # except EmptyPage:
    #     num = page.page(page.num_pages)
    books = Books.objects.all().order_by('id')  # 导入的Article模型
    p = Paginator(books, 2)  # 分页，10篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        book_list = books  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        book_list = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page
        }
    return render(request,'book.html',{'data': data, 'num': book_list})

def booktype(request):
    all = Booktype.objects.all()
    return render(request,'booktype.html',{'all':all})

def booklink(request,id):
    type = Booktype.objects.get(pk = id)
    li = Books.objects.filter(typeid=type)
    return render(request,'book.html',{'num':li})

#测试Redis存储
def test_redis(request):
    #使用缓存对象,操作Redis
    cache.set('name','tom',60) #存
    print(cache.has_key('name'))#判断
    print(cache.get('name'))#获取

    return HttpResponse("测试Redis")

# 发送短信
def send_sms(request):
    #接口地址:/duanxin/send_sms/?phone=xxxx
    # 1 获取手机
    phone = request.GET.get('phone')
    print('手机:'+phone)
    # 2 生成6位随机码
    code = aliyunsms.get_code(6, False)
    # 3 缓存到redis
    cache.set(phone,code,30*60)#60s有效
    print('是否写入redis成功:',cache.has_key(phone))
    print('打印code:',cache.get(phone))
    # 4 发短信
    result = aliyunsms.send_sms(phone, code)
    return HttpResponse(result)

#短信验证
def  check_sms(request):
    #/duanxin/check_sms/?phone=xxx&code=xx
    # 1 后去电话和code
    phone = request.GET.get('phone')
    code = request.GET.get('code')
    # 2 获取Resis中code
    cache_code = cache.get(phone)
    # 3 判断
    if code == cache_code:
        return  restful.ok("OK", data=None)
    else:
        return restful.page_error("False", data=None)






#验证码刷新
def img_refresh(request):
    if not request.is_ajax():
        return HttpResponse('不是Ajax请求')
    new_key = CaptchaStore.generate_key()
    to_json_response = {
        'hashkey': new_key,
        'image_url': captcha_image_url(new_key),
    }
    return HttpResponse(json.dumps(to_json_response))
#验证
def img_check(request):
    print('验证用户输入的图片验证码...')
    if request.is_ajax():
        code = request.GET.get('code')
        hashkey = request.GET.get('hashkey')
        cs = CaptchaStore.objects.filter(response=code, hashkey=hashkey)
        CS = CaptchaStore.objects.filter(challenge=code, hashkey=hashkey)
        print(code)
        print(CS)
        print(cs)
        if cs or CS:
            json_data={'status':1}
        else:
            json_data = {'status':0}
        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status':0}
        return JsonResponse(json_data)



def ajax(request):
    uname = request.GET['uname']
    print('用户名:', uname)
    # 链接数据库 User.objects.filter(uname='值')
    uname = Reader.objects.filter(username=uname).values()
    if uname:
        # admin已经被注册
        print(json.dumps({'result': 'false'}))
        return HttpResponse(json.dumps({'result': 'false'}))
    else:
        # 向前台返回的是json结果
        return HttpResponse(json.dumps({'result': 'ok'}))


def ajax_html(request):
    return render(request, 'ajax.html')











