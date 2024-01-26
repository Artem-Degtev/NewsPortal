from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.http import HttpResponse
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category
from django.shortcuts import redirect, get_object_or_404
import logging
import logging.handlers
from django.utils.log import RequireDebugFalse, RequireDebugTrue


# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание общего форматтера
common_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Создание обработчика для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(common_formatter)

# Создание обработчика для файла
file_handler = logging.FileHandler('general.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(common_formatter)

# Добавление обработчиков к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Создание обработчика для уровня WARNING
warning_handler = logging.StreamHandler()
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(common_formatter)

# Добавление обработчика к логгеру
logger.addHandler(warning_handler)

# Создание обработчика для уровня ERROR
error_handler = logging.StreamHandler()
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(common_formatter)

# Добавление обработчика к логгеру
logger.addHandler(error_handler)

# Создание фильтров для отладочных сообщений
class DebugFilter(logging.Filter):
    def filter(self, record):
        return not getattr(record, 'is_debug', False)

# Получение логгеров
django_server_logger = logging.getLogger('django.server')
django_template_logger = logging.getLogger('django.template')
django_db_logger = logging.getLogger('django.db.backends')
django_security_logger = logging.getLogger('django.security')

# Добавление обработчиков к логгерам
django_server_logger.addHandler(console_handler)
django_template_logger.addHandler(console_handler)
django_db_logger.addHandler(console_handler)
django_security_logger.addHandler(console_handler)

# Добавление фильтров к логгерам
django_server_logger.addFilter(DebugFilter())
django_template_logger.addFilter(DebugFilter())
django_db_logger.addFilter(DebugFilter())
django_security_logger.addFilter(DebugFilter())

def index(request):
    logger.info('INFO')
    news = New.objects.all()
    return render(request, 'index.html', context={'news': news})

def detail (request, slug):
    news = New.objects.all()
    new = New.objects.get(slug__iexact=slug)
    return render(request, 'details.html', context={'new': new, 'news': news})


class PostList(ListView):
    model = Post
    ordering = 'title'
    # queryset = Product.objects.filter(
    #     price_lt=300
    # )
    template_name = 'News.html'
    context_object_name = 'news'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Новые новости каждый день!"
        return context




class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')



@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        postCategory_id = request.POST.get('postCategory_id')
        postCategory = Category.objects.get(id=postCategory_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=postCategory)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=postCategory,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )