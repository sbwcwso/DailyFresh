"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from alipay import AliPay

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xa1$qs6-nw$5a1!e-!%ztnsb+^1t7%wi$bru!ik)%x39iehmz#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'haystack',  # 注册全文检索框架
    'user',
    'cart',
    'goods',
    'order',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        # 'OPTIONS': {'isolation_level': None},
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/var/www/dailyfresh/static'


# 富文本编辑器配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'width': 600,
    'height': 400,
}

# django 认证系统使用的模型类
AUTH_USER_MODEL = 'user.User'

# 发送邮件的邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'  # tp　服务器
EMAIL_PORT = 25  # 端口号
EMAIL_HOST_USER = 'lijunjie_auto@163.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'G9rdX79vgTssSdpG'  # 在邮箱中设置的客户端授权密码
EMAIL_FROM = '天天生鲜<lijunjie_auto@163.com>'  # 收件人看到的发件人

# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 配置 session 储存在缓存中
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 登录界面地址
LOGIN_URL = '/user/login'

# 设置 django 的文件储存类
DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'

# 设置 fastDFS 的使用的 client_conf 文件路径
FDFS_CLIENT_CONF = './utils/fdfs/client.conf'

# 设置 fastDFS 储存服务器上 nginx 的 ip 和端口号
# FDFS_URL = 'http://127.0.0.1:8888/'
FDFS_URL = 'http://picture.alijunjiea.com/'

# todo　jieba　分词的进一步完善，如将猪肉拆分为猪和肉
# 全文检索框架配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# 每页显示的搜索结果的页数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 3

# todo: alipay 初始化
APP_PRIVATE_KEY_STRING = open(os.path.join(BASE_DIR, 'apps/order/app_private_key.pem')).read()
ALIPAY_PUBLIC_KEY_STRING = open(os.path.join(BASE_DIR, 'apps/order/alipay_public_key.pem')).read()
# alipay初始化
ALIPAY = AliPay(
    appid='2016092800615022',
    app_notify_url=None,  # 默认回调url
    app_private_key_string=APP_PRIVATE_KEY_STRING,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,
    sign_type='RSA2',  # RSA 或者 RSA2
    debug=True,  # 默认False
)

# Solve Forbidden (CSRF cookie not set.): /order/notify
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


