from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from account_module.forms import AddEducationProduct
from account_module.models import UserModel
from product_module.forms import CommentForm
from product_module.models import Product, ProductCategory, ProductComment, UserFavoriteProducts


@method_decorator(login_required(login_url=reverse_lazy("login_view")), name='dispatch')
class ProductListView(ListView):
    template_name = 'product_list_view.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = ProductCategory.objects.filter(is_active=True)
        context['categories'] = category
        return context

    def get_queryset(self):
        category = self.request.GET.get('category')
        # print(category)
        if category:
            return Product.objects.filter(category__url_title__iexact=category, is_active=True)
        return Product.objects.filter(is_active=True).all()

        # def get_success_url(self):
    #     next_url = self.request.GET.get('next')
    #     if next_url:
    #         return next_url
    #     return reverse_lazy('product_list')


@method_decorator(login_required(login_url=reverse_lazy("login_view")), name='dispatch')
class ProductDetailView(DetailView):
    template_name = 'product_detail_page.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = self.object
        comments = ProductComment.objects.filter(product=product, is_accepted=True)
        context['comments'] = comments
        context['comments_count'] = comments.count()
        context['comment_form'] = CommentForm
        return context


@method_decorator(login_required(login_url=reverse_lazy('login_view')), name='dispatch')
class AddNewPost(CreateView):
    model = Product, UserModel
    form_class = AddEducationProduct
    template_name = 'add_post_page.html'
    success_url = reverse_lazy('user_panel_dashboard')

    def form_valid(self, form):
        if form.instance.owner is None:
            form.instance.owner = self.request.user

        if form.instance.is_free:
            free_category = ProductCategory.objects.get_or_create(url_title='free')[0]
            form.instance.category = free_category
        return super().form_valid(form)


def add_product_comment(request: HttpRequest):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = request.POST.get('product')
            user = request.user.id
            parent_id = request.POST.get('parent')
            comment = request.POST.get('text')

            if not product_id or not comment:
                messages.error(request, 'لطفا تمامی فیلد هارا پر کنید')
                return redirect(reverse_lazy('product_detail'))
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, 'محصول مورد نظر پیدا نشد')
                return redirect(reverse_lazy('product_detail'))

            parent = None
            if parent_id:
                parent = ProductComment.objects.get(id=parent_id)

            new_comment = ProductComment(product=product, parent=parent, user_id=user, text=comment, is_accepted=True)
            new_comment.save()
            print(new_comment)
            # context = {
            #     'product': product,
            #     'comments': comment,
            # }

            return redirect(reverse_lazy('product_detail', kwargs={'slug': product.slug}))

    return redirect(reverse_lazy('product_list'))


def add_product_to_favorite(request: HttpRequest, product_id: int):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            # favorite_products = request.session.get('favorite_products', [])
            if request.user.is_authenticated:
                favorite_products, created = UserFavoriteProducts.objects.get_or_create(user=request.user,
                                                                                        product=product)

            return redirect(reverse_lazy('add_product_to_favorite', kwargs={'product_id': product_id}))

        except Product.DoesNotExist:
            return redirect(reverse_lazy('user_panel_dashboard'))

    return redirect(reverse_lazy('user_panel_dashboard'))


def user_favorite_products(request: HttpRequest):
    if request.user.is_authenticated:
        favorite_products = UserFavoriteProducts.objects.filter(user=request.user)

        # products = Product.objects.filter(id__in=favorite_products)

        context = {'fav_products': favorite_products}

        return render(request, 'user_favorite_products.html', context)
    else:
        return redirect('login_view')
