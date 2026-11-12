from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/unpublish/", views.ProductUnpublishView.as_view(), name="product_unpublish"),
    path("category/<int:pk>/", views.ProductsByCategoryView.as_view(), name="category_products"),
    path("category/<slug:slug>/", views.ProductsByCategoryView.as_view(), name="category_products_slug"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]