from django.urls import path
from . import views
''' 
GET / => starting page lists most recent posts and welcome text
GET /posts => all posts (all posts)
GET /posts/<slug> => post details
GET / posts/update/<slug>

'''

urlpatterns = [
    path('', views.IndexView.as_view(), name='starting-page'),
    path('posts/', views.PostListView.as_view(), name='posts-page'),
    path('posts/create/', views.PostCreateView.as_view(), name='create-post'),
    path('posts/update/<slug:slug>/', views.PostUpdateView.as_view(), name='update-post'),
    path('posts/delete/<slug:slug>/', views.PostDeleteView.as_view(), name='delete-post'),
    path('posts/read-later/', views.ReadLaterView.as_view(), name='read-later'),
    path('posts/read-later/remove/', views.ReadLaterView.remove_saved_posts, name='remove-stored-posts'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail-page'),
]
