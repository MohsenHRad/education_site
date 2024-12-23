from datetime import timezone

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView

from account_module.models import UserModel
from product_module.models import Product
from .forms import ForgetPasswordForm, ChangePasswordForm, UserEditProfileForm, AddEducationProduct


# Create your views here.

class RegisterView(CreateView):
    template_name = 'register_form.html'
    model = UserModel
    fields = ['username', 'email', 'password']
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


def UserPanleView(request: HttpRequest):
    # user = UserModel.objects.get(username=request.user)
    return render(request, 'user_dashboard.html')


class UserLoginView(LoginView):
    template_name = 'login_form.html'
    success_url = reverse_lazy('home_page')

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return self.success_url
    # def form_valid(self, form):
    #     user_name = form.cleaned_data['username']
    #     user_password = form.cleaned_data['password']
    #
    #     user_authenticated


class UserLogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect('login_view')


class UserForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm()
        context = {
            "forget_password_form": forget_password_form,
        }
        return render(request, 'forget_pass_form.html', context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data['user_email']
            user: UserModel = UserModel.objects.filter(email__iexact=user_email).first()
            if user is None:
                forget_password_form.add_error('user_email', 'اطلاعات وارد شده صحیح نمیباشد')
            else:
                # print(request.session.items())
                request.session['user_email'] = user_email
                return redirect(reverse('change_password_view'))

        context = {
            "forget_password_form": forget_password_form
        }
        return render(request, 'forget_pass_form.html', context)


class UserChangePasswordView(View):
    def get(self, request: HttpRequest):
        change_password_form = ChangePasswordForm()
        context = {
            'change_password_form': change_password_form
        }
        return render(request, 'change_pass_form.html')

    def post(self, request: HttpRequest):
        change_password_form = ChangePasswordForm(request.POST)
        user_email = request.session.get('user_email')
        print(user_email)
        user: UserModel = UserModel.objects.filter(email__iexact=user_email).first()
        if change_password_form.is_valid():
            new_password = change_password_form.cleaned_data['user_new_password'].lower()
            confirm_new_password = change_password_form.cleaned_data['user_new_password_confirm'].lower()
            print(new_password)
            print(confirm_new_password)
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                logout(request)
                return redirect(reverse('login_view'))
            else:
                change_password_form.add_error('user_new_password_confirm', 'اطلاعات وارد شده مطابقت ندارد')

        context = {
            'change_password_form': change_password_form
        }
        return render(request, "change_pass_form.html", context)


class UserEditProfile(View):
    def get(self, request: HttpRequest):
        current_user = UserModel.objects.filter(id=request.user.id).first()
        edit_form = UserEditProfileForm(instance=current_user)

        context = {

            'edit_form': edit_form,
            'user': current_user,
        }

        return render(request, 'user_edit_profile.html', context)

    def post(self, request: HttpRequest):
        current_user = UserModel.objects.filter(id=request.user.id).first()
        edit_form = UserEditProfileForm(request.POST, request.FILES, instance=current_user)
        print(current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect(reverse('user_panel_dashboard'))
        context = {
            'edit_form': edit_form,
            'user': current_user,
        }
        return render(request, 'user_edit_profile.html', context)



