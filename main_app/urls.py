from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('instruments/', views.instruments_index, name='index'),
    path('instruments/<int:instrument_id>/', views.instruments_detail, name='detail'),
    path('instruments/create/', views.InstrumentCreate.as_view(), name='instruments_create'),
    path('instruments/<int:pk>/update/', views.InstrumentUpdate.as_view(), name='instruments_update'),
    path('instruments/<int:pk>/delete/', views.InstrumentDelete.as_view(), name='instruments_delete'),
    path('instruments/<int:instrument_id>/add_practice/', views.add_practice, name='add_practice'),
    path('instruments/<int:instrument_id>/add_photo/', views.add_photo, name='add_photo'),
    path('instruments/<int:instrument_id>/assoc_product/<int:product_id>/', views.assoc_product, name='assoc_product'),
    path('instruments/<int:instrument_id>/dissoc_product/<int:product_id>/', views.dissoc_product, name='dissoc_product'),
    path('products/', views.ProductList.as_view(), name='products_index'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='products_detail'),
    path('products/<int:pk>/update/', views.ProductUpdate.as_view(), name='products_update'),
    path('products/<int:pk>/delete/', views.ProductDelete.as_view(), name='products_delete'),
    path('products/create/', views.ProductCreate.as_view(), name='products_create'),
]