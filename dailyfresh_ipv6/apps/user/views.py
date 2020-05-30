from django.shortcuts import render, redirect
from user.models import User, Address
from django.urls import reverse
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_task.tasks import send_register_active_email
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from goods.models import GoodsSKU
from order.models import OrderGoods, OrderInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class RegisterView(View):
    """注册操作"""
    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""
        # 1. 获取登录信息
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2. 登录信息校验, 为了减少 post 请求的次数,可以在表单中加入验证,阻止表单的默认行为
        # 验证是否输入所有的数据
        if not all([user_name, pwd, cpwd, email]):
            return render(request, "register.html", {'error_msg': "注册信息输入不完整"})
        # 检查用户名长度是否合法
        if len(user_name) < 5 or len(user_name) > 20:
            return render(request, "register.html", {'error_msg': "请输入5-20个字符的用户名"})
        # 检查用户名是否已存在
        try:
            foo = User.objects.get(username=user_name)
        except User.DoesNotExist:
            foo = None
        if foo is not None:
            return render(request, "register.html", {'error_msg': "用户名已存在"})
        # 检查密码的长度是否合法
        if len(pwd) < 8 or len(pwd) > 20:
            return render(request, "register.html", {'error_msg': "请输入8-20个字符的密码"})
        # 检查两次输入的密码是否相同
        if pwd != cpwd:
            return render(request, "register.html", {'error_msg': "两次输入的密码不一致"})
        # 检查邮箱格式是否正确
        if not re.match(r"^[a-z0-9][a-zA-Z0-9_.\-]*@[a-z0-9\-]+(\.[a-zA-Z]{2,5}){1,2}$", email):
            return render(request, 'register.html', {'error_msg': "邮箱格式不正确"})
        # 检查邮箱是否已注册
        # try:
        #     foo = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     foo = None
        # if foo is not None:
        #     return render(request, 'register.html', {'error_msg': "邮箱已注册"})
        # 检查是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'error_msg': "请同意用户协议"})

        # 3. 更新数据库
        user = User.objects.create_user(user_name, email, pwd)
        user.is_active = 0
        user.save()

        # 4. 发送激活邮件,包含激活链接: http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息,并且身份信息需要进行加密处理

        # 加密用户的身份信息,生成激活 token, 设置过期时间为 3600 秒
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # byte
        token = token.decode()

        # 发送邮件
        send_register_active_email.delay(email, user_name, token)

        return HttpResponse("<h2>激活邮件已发送至邮箱%s,请前往邮箱激活.</h2><br><a href='/'>返回首页<a>" % email)


# /user/active/token
class ActiveView(View):
    """激活帐户"""
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
        except SignatureExpired:
            return HttpResponse("激活链接已过期")

        # 获取用户 id, 并根据用户 id 获取相关信息
        user_id = info['confirm']
        user = User.objects.get(id=user_id)
        user.is_active = 1
        user.save()

        # 激活成功,返回登录页面
        return HttpResponse("<h2>激活成功.</h2><br><a href='/user/login'>前往登录界面<a>")


# /user/login
class LoginView(View):
    """用户登录页面"""
    def get(self, request):
        """显示登录页面"""
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ""
            checked = ""
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """校验登录信息"""
        # 1. 获取用户信息
        username = request.POST.get('username')
        pwd = request.POST.get("pwd")
        remember = request.POST.get("remember")
        # 2. 校验用户信息
        user = authenticate(username=username, password=pwd)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                # 登录成功,保存登录状态信息
                login(request, user)
                # 获取登录成功后要跳转的地址,默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))
                response = redirect(next_url)
                # 处理是否记住用户名
                if remember == "on":
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                return render(request, "login.html", {'error_msg': '帐户末激活'})
        else:
            # the authentication system was unable to verify the username and password
            return render(request, "login.html", {'error_msg': '用户名或密码错误'})


# /user/logout
class LogOutView(View):
    """登出视图"""
    def get(self, request):
        logout(request)
        next_url = request.GET.get('next', reverse('goods:index'))
        # 重定向到指定的页面,默认重定向到首页
        return redirect(next_url)


# /user
class UserInfoView(LoginRequiredMixin, View):
    """用户中心-信息"""
    def get(self, request):
        """显示页面信息"""
        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户浏览的历史记录
        con = get_redis_connection("default")
        history_key = 'history_%d' % user.id

        # 获取用户浏览的最近五个商品
        sku_ids = con.lrange(history_key, 0, 4)
        # 按顺序查询
        goods_li = list()
        for sku_id in sku_ids:
            goods_li.append(GoodsSKU.objects.get(id=sku_id))

        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li,
                   }
        return render(request, "user_center_info.html", context)


# /user/order/page_num
class UserOrderView(LoginRequiredMixin, View):
    """显示用户中心-订单页面"""
    def get(self, request, page):
        # 查询相关数据
        orders = OrderInfo.objects.filter(user=request.user).order_by("-create_time")
        all_orders = list()
        for order in orders:
            order.goods = OrderGoods.objects.filter(order=order)
            order.total_price = 0
            for good in order.goods:
                order.total_price += good.price
            order.total_price += order.transit_price
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            all_orders.append(order)

        # 分页相关
        paginator = Paginator(all_orders, 2)  # Show 2 contacts per page
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)

        # 控制商品显示的页码数量,最多只显示 5 页
        page = current_page.number
        total_page = paginator.num_pages
        if total_page < 5:
            page_range = range(1, total_page + 1)
        elif page < 3:
            page_range = range(1, 6)
        elif page > total_page - 2:
            page_range = range(total_page - 4, total_page + 1)
        else:
            page_range = range(page - 2, page + 3)
        return render(request, "user_center_order.html", {'page': 'order',
                                                          'current_page': current_page,
                                                          'page_range': page_range,
                                                          })


# /user/site
class UserSiteView(LoginRequiredMixin, View):
    """用户中心-地址"""
    def get(self, request):
        """显示页面"""
        default_address = Address.objects.get_default_address(request.user)
        all_address = Address.objects.filter(user=request.user)
        return render(request, "user_center_site.html",
                      {'page': 'site',
                       'default_address': default_address,
                       'all_address': all_address})

    def post(self, request):
        """添加新地址"""
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, "user_center_site.html", {'page': 'site', 'error_msg': '信息不完整'})

        if not re.match(r"^1[34578][0-9]{9}$", phone):
            return render(request, "user_center_site.html", {'page': 'site', 'error_msg': '手机号格式不正确'})

        # 业务处理
        # 判断是否有默认地址,如果没有,则将当前地址设为默认地址
        user = request.user
        address = Address.objects.get_default_address(user)
        if address is None:
            is_default = True
        else:
            is_default = False

        new_address = Address.objects.create(user=user,
                                             receiver=receiver,
                                             addr=addr,
                                             zip_code=zip_code,
                                             phone=phone,
                                             is_default=is_default)
        new_address.save()
        # 返回应答,重定向到地址页
        return redirect(reverse('user:site'))
