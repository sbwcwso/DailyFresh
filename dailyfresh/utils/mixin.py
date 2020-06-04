from django.contrib.auth.decorators import login_required


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        # 通过多继承, 调用父类的 as_view
        view = super().as_view(**initkwargs)
        return login_required(view)  # 进行封装
