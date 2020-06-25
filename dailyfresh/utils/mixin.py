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


def get_page_range(paginator, current_page):
    """
    自定义分页逻辑

    1. 总页数小于 5 页，则页面上显示所有页码
    2. 当前页是前 3 页，则显示 1 ~ 5 页
    3. 当前页是后 3 页，则显示后 5 页
    4. 其它情况下，显示当前面的前 2 页，当前页，当前页的后 2 页

    :param paginator: 分页对象
    :param current_page: 当前页
    :return: page_range[Iterable]:  要显示的页码范围
    """
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
    return page_range


class ListViewMixin:
    """
    为 ListView 的 context 添加要显示的页码范围 page_range
    """

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        context = super().get_context_data(objeclist=object_list, **kwargs)
        page_range = get_page_range(context['paginator'], context['page_obj'])
        context.update({'page_range': page_range})
        return context


class SearchViewMixin:
    """
    为 SearchViewMixin 的 context 添加要显示的页码范围  page_range
    """
    def get_context(self):
        context = super().get_context()

        page_range = get_page_range(context['paginator'], context['page'])
        context.update({'page_range': page_range})
        return context

