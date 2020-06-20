from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class LoginRequiredMixin:
    """
    验证是否登录的混入类
    """
    @classmethod
    def as_view(cls, **initkwargs):
        # 通过多继承, 调用父类的 as_view
        view = super().as_view(**initkwargs)
        # 调用装饰器进行封装
        return login_required(view)


class ListViewMixin:
    """
    改写分页逻辑
    """
    @staticmethod
    def get_paginate(queryset, page_size, page):
        """
        自定义分页逻辑

        1. 总页数小于 5 页，则页面上显示所有页码
        2. 当前页是前 3 页，则显示 1 ~ 5 页
        3. 当前页是后 3 页，则显示后 5 页
        4. 其它情况下，显示当前面的前 2 页，当前页，当前页的后 2 页

        :param queryset: 查询集集合
        :param page_size: 每页显示的数目
        :param page: 当前页的页码
        :return: current_page[paginator.Page]:  当前页，类型为
        :return: page_range[Iterable]:  要显示的页码范围
        """
        paginator = Paginator(queryset, page_size)
        try:
            current_page = paginator.page(page)
            print(type(current_page))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)

        # 控制显示的页码数量,最多只显示 5 页
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
        return current_page, page_range

    def paginate_queryset(self, queryset, page_size):
        """
        添加分页逻辑

        1. 总页数小于 5 页，则页面上显示所有页码
        2. 当前页是前 3 页，则显示 1 ~ 5 页
        3. 当前页是后 3 页，则显示后 5 页
        4. 其它情况下，显示当前面的前 2 页，当前页，当前页的后 2 页
        """

        """Paginate the queryset, if needed."""
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

        return self.get_paginate(queryset, page_size, page)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        current_page, page_range = self.paginate_queryset(queryset, page_size)
        context = {
            'current_page': current_page,
            'page_range': page_range,
        }
        context.update(kwargs)
        return context



