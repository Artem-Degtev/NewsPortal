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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# Создание файлового обработчика для записи логов в файл general.log
file_handler = logging.FileHandler('general.log')
file_handler.setLevel(logging.INFO)

# Создание форматтера для задания формата вывода в файл
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Добавление файлового обработчика к основному логгеру
logger.addHandler(file_handler)

# Создание файлового обработчика для записи логов уровня ERROR и выше в файл errors.log
errors_file_handler = logging.FileHandler('errors.log')
errors_file_handler.setLevel(logging.ERROR)

# Создание форматтера для задания формата вывода в файл errors.log
errors_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s\n%(exc_info)s')
errors_file_handler.setFormatter(errors_formatter)

# Добавление файлового обработчика к определенным регистраторам Django
django_loggers = ['django.request', 'django.server', 'django.template', 'django.db.backends']
for logger_name in django_loggers:
    logger = logging.getLogger(logger_name)
    logger.addHandler(errors_file_handler)

# Создание файлового обработчика для записи логов из регистратора django.security
security_file_handler = logging.FileHandler('security.log')
security_file_handler.setLevel(logging.DEBUG)  # Установите уровень логирования по необходимости

# Создание форматтера для задания формата вывода в файл security.log
security_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
security_file_handler.setFormatter(security_formatter)

# Добавление файлового обработчика к регистратору django.security
security_logger = logging.getLogger('django.security')
security_logger.addHandler(security_file_handler)


# Создание почтового обработчика для отправки сообщений уровня ERROR и выше на почту
mail_handler = logging.handlers.SMTPHandler(
    mailhost=('smtp.yandex.ru', 465),
    fromaddr='degtevag@yandex.ru',
    toaddrs='artemdegtev@gmail.ru',
    subject='Error from your application',
    credentials=('degtevag', 'pflmrrodkpbwmqdd'),
    secure=()
)
mail_handler.setLevel(logging.ERROR)

# Создание форматтера для задания формата вывода на почту
mail_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s')
mail_handler.setFormatter(mail_formatter)

# Добавление почтового обработчика к регистраторам django.request и django.server
django_request_logger = logging.getLogger('django.request')
django_request_logger.addHandler(mail_handler)

django_server_logger = logging.getLogger('django.server')
django_server_logger.addHandler(mail_handler)

# Установка фильтрации для разных обработчиков в зависимости от значения DEBUG
class DebugFilter(logging.Filter):
    def filter(self, record):
        return not getattr(record, 'is_debug', False)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Применение фильтра к обработчику для вывода логов в консоль
console_handler.addFilter(DebugFilter())

# Добавление обработчика к основному логгеру
logger.addHandler(console_handler)

# Применение фильтра к обработчикам для файла и почты
file_handler.addFilter(DebugFilter())
mail_handler.addFilter(DebugFilter())

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