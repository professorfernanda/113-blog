from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Post, Status
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        draft_status = Status.objects.get(name="draft")
        form.instance.status = draft_status
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = "posts/detail.html"
    model = Post


class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context["post_list"] = Post.objects.filter(
            status = published_status
        ).order_by("created_on").reverse()
        context["my_name"] = "Fernanda Murillo"
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    

class DraftListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="draft")
        context["post_list"] = Post.objects.filter(
            status = draft_status
        ).filter(
            author = self.request.user
        ).order_by("created_on").reverse()
        return context
    
class ArchieveListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archieve_status = Status.objects.get(name="archived")
        context["post_list"] = Post.objects.filter(
            status = archieve_status
        ).filter(
            author = self.request.user
        ).order_by("created_on").reverse()
        return context