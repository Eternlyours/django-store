from django.urls import path
from .views import ProductDetailView, ProductListView


urlpatterns = [
    path('', ProductListView.as_view()),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]