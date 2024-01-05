from django.urls import include, path
from . import views
from django.urls import reverse_lazy

app_name = 'blog'

urlpatterns = [
    
    path('', views.index, name='index'),
    
    path('about/', views.about, name='about'),
    
    path('login/', views.SuperUserLoginView.as_view(), name='login'),
    
     path('logout/', views.SuperUserLogoutView.as_view(), name='logout'),
    
    path('list', views.PostListView.as_view(), name='post_list'),
   
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    path('create/', views.PostCreateView.as_view(), name='post_new'),
    
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name='post_edit'),
    
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_remove'),
    
    path('comment/<int:pk>/', views.add_comment_to_post, name='add_comment_to_post'),
    
    path('draft/', views.DraftListView.as_view(), name='post_draft_list'),
    
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
]
