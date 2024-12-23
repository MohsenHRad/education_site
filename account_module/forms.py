from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core import validators

from account_module.models import UserModel
from product_module.models import Product


class ForgetPasswordForm(forms.Form):
    user_email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'place_holder': 'ایمیل شما'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ],
        error_messages={
            "required": 'لطفا ایمیل خود را وارد کنید ',
            "invalid": "لظفا ایمیل معتبر وارد کنید "
        }
    )


class ChangePasswordForm(forms.Form):
    user_new_password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور شما'
        }),
        validators=[

            validate_password,
        ],
        error_messages={
            "required": 'لطفا رمز عبور خود را وارد کنید ',
            "invalid": "لظفا رمز عبور معتبر وارد کنید ",
            "min_length": 'رمز عبور تایید شده باید حداقل 8 کاراکتر باشد',
        }
    )
    user_new_password_confirm = forms.CharField(
        label='تایید رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور شما'
        }),
        validators=[
            validate_password,
        ],
        error_messages={
            "required": 'لطفا تایید رمز عبور خود را وارد کنید ',
            "invalid": "لظفا رمز عبور معتبر وارد کنید "
        }
    )


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'user_avatar']
        labels = {'نام کاربری', 'نام', 'نام خانوادگی', 'ایمیل', 'تصویر پروفایل'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام ', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی', }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل', }),
            'user_avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'عکس', }),
        }


class AddEducationProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'owner', 'subject', 'short_description', 'price', 'category', 'image', 'is_active',
                  'is_free']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام محصول', }),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام در url ', }),
            'owner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نویسنده ', }),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موضوع', }),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیجات کوتاه', }),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'قیمت', }),
            'category': forms.Select(
                attrs={'class': 'form-control'},

            ),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'عکس', }),
        }
