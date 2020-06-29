#!/bin/sh

# 启动fastdfs
sudo service fdfs_trackerd start
sudo service fdfs_storaged start

# 启动nginx 服务，指定配置文件的位置
sudo /usr/local/nginx/sbin/nginx -c /home/lijunjie/Documents/Django/DailyFresh/conf/nginx/nginx.conf

# 启动　redis
sudo redis-server /etc/redis/redis.conf

# 启动 celery
/home/lijunjie/.virtualenvs/DailyFresh/bin/celery --workdir="/home/lijunjie/Documents/Django/DailyFresh_Celery/dailyfresh" -A celery_task.tasks worker -l info > /tmp/celery.log 2>&1 &

# 启动 uwsgi
/home/lijunjie/.virtualenvs/DailyFresh/bin/uwsgi --ini /home/lijunjie/Documents/Django/DailyFresh/conf/uwsgi/uwsgi.ini