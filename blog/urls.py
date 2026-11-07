
from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="blogpost_list"),
    path("<int:pk>/", views.BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("create/", views.BlogPostCreateView.as_view(), name="blogpost_create"),
    path("<int:pk>/update/", views.BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("<int:pk>/delete/", views.BlogPostDeleteView.as_view(), name="blogpost_delete"),
]