from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.PostCategoryView.as_view(), name='post_category'),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
]
