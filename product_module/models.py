from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from account_module.models import UserModel


# Create your models here.
class ProductCategory(MPTTModel):
    name = models.CharField(max_length=300, db_index=True, verbose_name='نام')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return f'{self.name} - {self.url_title}'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام محصول')
    slug = models.SlugField(blank=False, null=False, db_index=True, max_length=200, unique=True,
                            verbose_name='مشخصه در سایت')
    owner = models.CharField(max_length=100, verbose_name='مدرس')
    subject = models.CharField(max_length=100, null=False, blank=False, verbose_name='موضوع')
    short_description = models.TextField(verbose_name='توضیحات کوتاه ')
    price = models.IntegerField(null=False, blank=False, verbose_name='قیمت')
    image = models.ImageField(null=True, blank=True, upload_to="product_module/static/images", verbose_name='تصویر')
    created_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='تاریخ ایجاد')
    view = models.IntegerField(null=True, blank=True, default=1, verbose_name='تعداد مشاهده')
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    is_free = models.BooleanField(default=False, verbose_name='رایگان')
    time = models.IntegerField(default=1, verbose_name='زمان آموزش')
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE, blank=True,
                                 null=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def slugify_title(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + self.owner

    class Meta:
        verbose_name = 'دسته محصولات آموزشی',
        verbose_name_plural = 'دسته های محصولات آموزشی'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, related_name='product_comment', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='parent_comment', on_delete=models.CASCADE,
                               verbose_name='والد')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    created_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='تاریخ ایجاد')
    text = models.TextField(verbose_name='متن نظر')
    is_accepted = models.BooleanField(verbose_name='تایید شده')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظرات کاربران'


class UserFavoriteProducts(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='یوزر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    class Meta:
        unique_together = ('user', 'product')
