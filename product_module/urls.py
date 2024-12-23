from django.urls import path

from product_module import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('add-product-comment', views.add_product_comment, name='add_product_comment'),
    path('post/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-new-post/', views.AddNewPost.as_view(), name='add_new_post'),
    path('favorite-product/<int:product_id>', views.add_product_to_favorite, name='add_product_to_favorite'),
    path('favorites/', views.user_favorite_products, name='user_favorite_products'),
]
