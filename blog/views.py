from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

def about(request):
    return render(request, 'blog/about.html')

class SuperUserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('blog:post_new')
    def dispatch(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.success_url)
            else:
                messages.error(request, 'Invalid Credentials. Please Contact Admin.')
                return redirect('blog:login')
        return super().dispatch(request, *args, **kwargs)

class SuperUserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'
    login_url = '/login/'
    next_page = reverse_lazy('blog:login')
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs) 
    
class PostListView(ListView):
    model = Post
    def get_queryset(self):
        user=self.request.user
        if user.is_authenticated:
            return Post.objects.filter().order_by('-published_date')
        else:
            return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
 
class PostCreateView(LoginRequiredMixin, CreateView):
    fields = ['title', 'text']
    template_name = 'blog/post_form.html'
    login_url = '/login/'
    redirect_field_name ='blog/post_list.html'
    model = Post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name ='blog/post_detail.html'
    form_class = PostForm
    model = Post
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_confirm_delete.html'

class DraftListView(LoginRequiredMixin, ListView): 
    template_name = 'blog/post_draft_list.html'
    login_url = '/login/'
    redirect_field_name ='blog:post_draft_list'
    model = Post 
    context_object_name = 'draft_list'
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author=self.request.user).order_by('-create_date')
 

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk) 
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=post.pk)




    
    
    
