#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/7/19 9:39 AM
# @Author  : Lijunjie
# @Site    : 
# @File    : upload_file
# @Software: PyCharm


import os
from fdfs_client.client import Fdfs_client


dirname = "/mnt/hgfs/CS/培训/14天天生鲜项目/dailyfresh/static/images"
client = Fdfs_client("/etc/fdfs/client.conf")

for main_dir, subdir, file_name_list in os.walk(dirname):
    for file_name in file_name_list:
        file = os.path.join(main_dir, file_name)
        with open(file, 'rb') as f_obj:
            res = client.upload_by_buffer(f_obj.read())
        print(file)
        print(res["Remote file_id"])
        client.delete_file(res['Remote file_id'])



