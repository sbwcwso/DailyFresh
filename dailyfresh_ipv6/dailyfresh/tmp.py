

# 分页相关
paginator = Paginator(skus, 3)  # Show 3 contacts per page
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