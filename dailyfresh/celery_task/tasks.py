# 加载配置项,在任务处理端需要加入
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner
from django.template import loader
import os

# 创建一个 Celery 类的实例对象
app = Celery('celery_tasks.task', broker="redis://192.168.10.108:6379/8")


@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    subject = "天天生鲜账户激活: %s" % username
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    message = ''
    begin_url = "http://dailyfresh.ignorelist.com/user/active/%s" % token
    html_message = """<h1>欢迎成为天天生鲜会员</h1><br />请点击以下链接激活您的账户:<br />
        <a href='%s'>%s</a><br /> 该激活链接 1 小时内有效""" % (begin_url, begin_url)
    send_mail(subject=subject, message=message, from_email=sender, recipient_list=receiver,
              html_message=html_message)


@app.task
def generate_static_index_html():
    """产生首页静态页面"""
    # 从 mysql 中查询商品的相关信息
    goods_types = GoodsType.objects.all()
    banners = IndexGoodsBanner.objects.all().order_by("index")
    for goods_type in goods_types:
        goods_type.titles = IndexTypeGoodsBanner.objects.filter(type=goods_type, display_type=0).order_by("index")
        goods_type.images = IndexTypeGoodsBanner.objects.filter(type=goods_type, display_type=1).order_by("index")
    promotion_banner = IndexPromotionBanner.objects.all().order_by("index")

    content_text = {
        "types": goods_types,
        "banners": banners,
        "promotion_banners": promotion_banner,
        "cart_num": 0,
    }

    # 加载模型文件
    temp = loader.get_template("static_index.html")
    # 模板渲染
    static_index_html = temp.render(content_text)

    # 生成首页对应的静态页面
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)

