from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import BlogForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from marketing.forms import EmailSignupForm
from urllib.parse import quote_plus


class PostListView(ListView):
    queryset = BlogPost.objects.order_by('-created_at')
    template_name = "blogs/home.html"
    context_object_name = 'queryset'
    ordering = ['-updated_at', '-created_at']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*kwargs)
        context['latest_post'] = BlogPost.objects.order_by("-created_at")[:10]
        context['form'] = EmailSignupForm()
        return context


class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blog-detail.html'

    def get_object(self):
        slug = self.kwargs.get('title_slug')
        return get_object_or_404(BlogPost, slug=slug)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['share_string'] = quote_plus(self.get_object().content)
    #     return context


class PostCreateView(SuccessMessageMixin, CreateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blogs/blog-form.html'
    success_message = 'Post added successfully!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blogs/blog-update.html'
    success_message = 'Post updated successfully!'

    def get_object(self):
        slug = self.kwargs.get('title_slug')
        return get_object_or_404(BlogPost, slug=slug)


class PostDeleteView(SuccessMessageMixin, DeleteView):
    model = BlogPost
    template_name = 'blogs/blog-delete.html'
    success_message = 'Post deleted successfully!'
    success_url = "/"

    def get_object(self):
        slug = self.kwargs.get('title_slug')
        return get_object_or_404(BlogPost, slug=slug)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = BlogPost.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset,
            'query': query,
        }
        return render(request, 'blogs/search_result.html', context)


# ! Function Based View for UserPost
# def user_posts(request, username):
#     queryset = BlogPost.objects.filter(author__username=username)
#     return render(request, 'blogs/user-posts.html', {'queryset': queryset, 'username': username})


class UserPost(ListView):
    model = BlogPost
    template_name = 'blogs/user-posts.html'
    paginate_by = 3
    context_object_name = 'queryset'
    ordering = ['-updated_at', '-created_at']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(author=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context
