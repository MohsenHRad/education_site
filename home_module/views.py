from django.core.paginator import Paginator
from django.views.generic import TemplateView

from product_module.models import Product


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        products = Product.objects.all().order_by('-created_date')
        pagination = Paginator(products, 2)
        page_number = self.request.GET.get('page', 1)
        page_obj = Paginator.get_page(pagination, page_number)

        context['page_obj'] = page_obj
        context['page_number'] = page_number
        context['pagination'] = pagination

        context['user'] = user
        context['products'] = products
        return context
