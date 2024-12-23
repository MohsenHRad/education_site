from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserModel(AbstractUser):
    user_avatar = models.ImageField(upload_to='uploads/images/profile', null=True, blank=True,
                                    verbose_name='عکس پروفایل')
    user_description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.email
