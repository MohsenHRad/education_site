from django.urls import path

from account_module import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('dashboard/', views.UserPanleView, name='user_panel_dashboard'),
    path('login/', views.UserLoginView.as_view(), name='login_view'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_view'),
    path('forget-pass/', views.UserForgetPasswordView.as_view(), name='forget_pass_view'),
    path('change-password/', views.UserChangePasswordView.as_view(), name='change_password_view'),
    path('edit_profile/', views.UserEditProfile.as_view(), name='edit_profile_view'),
]
