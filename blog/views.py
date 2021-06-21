from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.http import require_POST


# models
from .models import Comment, Post, Tag

# forms
from .forms import CommentForm, PostModelForm, CommentModelForm


# starting-page
class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-posted_at')[:3]

#################################################


# ---------- POST Views ----------------

class PostListView(ListView):
    template_name = 'blog/all-posts.html'
    queryset = Post.objects.all().order_by('-posted_at')
    # paginate_by = 3
    context_object_name = 'posts'


class PostDetailView(View):
    template_name = 'blog/post-detail.html'
    queryset = Post.objects.all()

    def get(self, request:HttpRequest, *args, **kwargs):
        post: Post = self.queryset.get(slug=kwargs['slug'])
        saved_posts = request.session.get('stored_posts')
        is_saved = False if not saved_posts else kwargs['slug'] in saved_posts
        context = {
            'post': post,
            'form': CommentModelForm(),
            'comments': post.comment_set.all().order_by('-created_at'),
            'is_saved': is_saved
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment: Comment = form.save(commit=False)
            comment.post = self.queryset.get(slug=kwargs['slug'])
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[kwargs['slug']]))

        post: Post = self.queryset.get(slug=kwargs['slug'])
        context = {
            'form': CommentModelForm(request.POST),
            'post': post,
            'comments': post.comment_set.all().order_by('-created_at')
        }
        return render(request, self.template_name, context)


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/create-post.html'
    form_class = PostModelForm
    success_url = reverse_lazy('posts-page')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostModelForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('posts-page')

    template_name = 'blog/create-post.html'

    extra_context = {
        'update_mode': True
    }

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete-post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts-page')


class ReadLaterView(View):
    template_name = 'blog/stored-posts.html'
    def get(self, request:HttpRequest):
        stored_posts:list = request.session.get('stored_posts')
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['stored_posts'] = []
            context['has_posts'] = False
        else:
            read_later_posts = Post.objects.filter(slug__in=stored_posts)
            context['stored_posts'] = read_later_posts
            context['has_posts'] = True

        return render(request, self.template_name, context)


    def post(self, request:HttpRequest):
        stored_posts = request.session.get('stored_posts', [])
        post_slug = request.POST.get('post_slug')
        
        if post_slug in stored_posts:
            post_index = stored_posts.index(post_slug)
            stored_posts.pop(post_index)
            request.session['stored_posts'] = stored_posts
            return HttpResponseRedirect(reverse('post-detail-page', args=[post_slug]))
        else:        
            stored_posts.append(post_slug)
            request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect(reverse('read-later'))

    @staticmethod
    def remove_saved_posts(request:HttpRequest):
        stored_posts = request.session.get('stored_posts', None)
        if stored_posts:
            del request.session['stored_posts']

        return HttpResponseRedirect(reverse('posts-page'))
        