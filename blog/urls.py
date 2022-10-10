from  django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from  django.urls import path, reverse_lazy
from .models      import Post, Category
from .forms       import PostUpdateForm
from .views       import PostList, CategoryList, CategoryPosts, LikeView, PostDetail, PostCreateView, CommentCreateView, CommentDelete

urlpatterns = [

# list posts
    path('post_list', PostList.as_view(), name ='post_list'),
    # path('list', ListView.as_view(
    #     model    = Post,
    #     ordering = ['-date'],
    # ),  name     ='post_list'),

# individual post detail
    path('post_detail/<int:pk>', PostDetail.as_view(), name='post_detail'),
    # path('detail/<int:pk>', DetailView.as_view(model = Post,), name='post_detail'),

# add / create post
    path('post_create', PostCreateView.as_view(), name='post_create'),
    # path('post_create', CreateView.as_view( 
    #     model         = Post,
    #     form_class    = PostCreateForm,
    #     template_name = 'blog/post_create.html',
    # ), name='post_create'),

 # edit/update post
    path('post_update/<int:pk>', UpdateView.as_view( 
        model         = Post,
        form_class    = PostUpdateForm,
        template_name = 'blog/post_update.html',
    ), name='post_update'),

# delete post
    path('delete/<int:pk>', DeleteView.as_view(
        model         = Post,
        template_name = 'blog/post_delete.html',
        success_url   = reverse_lazy('post_list'),
    ), name='post_delete'),

# create / add category
    path('category', CreateView.as_view( 
        model         = Category,
        template_name = 'blog/category_create.html',
        success_url   = reverse_lazy('category_list'),
        fields        = ('name',)
    ), name='category_create'),

# list of categories
    path('category_list', CategoryList, name='category_list'),

# # delete categories
#     path('category_delete', CategoryDelete, name='category_delete'),

# list posts of the selected category
    path('category/<str:category>', CategoryPosts, name='category_posts'),

# create likes on posts
    path('like/<int:post_id>', LikeView, name='like_post'),

# create comment
    path('comment_create/<int:post_pk>', CommentCreateView.as_view(), name='comment_create'),
    # path('list',            PostList.as_view(),   name='post_list'),
    # path('detail/<int:pk>', PostDetail.as_view(), name='post_detail'),

# delete post
    path('comment_delete/<int:comment_id>/<int:post_id>', CommentDelete, name='comment_delete'),

]
