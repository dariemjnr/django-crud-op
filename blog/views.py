from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from .form import PostForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)
from django.contrib.auth import login, logout
from django.utils.text import slugify
# Create your views here.

class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'blog_templates/list.html'

class PostCreateView(CreateView):
    template_name = 'blog_templates/form.html'
    form_class = PostForm
    queryset = Post.objects.all()

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:all')

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'blog_templates/detail.html'

    def get_object(self):
        slug__ = self.kwargs.get('slug')
        return get_object_or_404(Post, slug=slug__)

class PostUpdateView(UpdateView):
    template_name = 'blog_templates/form.html'
    queryset = Post.objects.all()
    form_class = PostForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:all')

class PostDeleteView(DeleteView):
    template_name = 'blog_templates/delete.html'
    queryset = Post.objects.all()

    def get_object(self):
        slug__ = self.kwargs.get('slug')
        return get_object_or_404(Post, slug=slug__)
    
    def get_success_url(self):
        return reverse_lazy('blog:all')

# Implemented a search Feature
def search(request, *args, **kwargs):
    search_result = request.POST.get('q')
    if not search_result is None:
        slug = slugify(search_result)
        lookup = Q(title__contains=search_result)|Q(slug__iexact=slug)|Q(body__icontains=search_result)
        obj = Post.objects.filter(lookup)
        context = {
            'object': obj
        }
    else:
        context ={
            'object': ''
        }
      
    return render (request, 'base.html', context)

# User Registration view
def register(request, *args, **kwargs):
    register = UserCreationForm(request.POST or None)
    if register.is_valid():
        register.save()
        return redirect('blog:all')
    context = {
        'register':register
    }
    return render(request, 'blog_templates/register.html', context)

# login View
def loginView(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('blog:all')
    else:
        form = AuthenticationForm(request)
    context = {
        'form':form
    }
    return render(request, 'blog_templates/login.html', context)

# logout view
def logoutView(request, *args, **kwargs):
    if request.POST:
        logout(request)
        return redirect('blog:login')
 
    return render(request, 'blog_templates/logout.html', {})
