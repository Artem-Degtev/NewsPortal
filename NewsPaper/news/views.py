from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post
from django.http import HttpResponse
from .filters import PostFilter


class NewsList(ListView):
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




class NewsDetail(DetailView):
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