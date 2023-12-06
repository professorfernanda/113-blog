from django.urls import path
from posts import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("new/", views.PostCreateView.as_view(), name="post_new"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("drafts/", views.DraftListView.as_view(), name="drafts"),
    path("archived/", views.ArchieveListView.as_view(), name="archived"),
]
