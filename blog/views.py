# from .forms  import PostForm
# from  django.contrib       import messages
# from  django.db            import transaction
from  django.views.generic import ListView, DetailView, CreateView
from  django.shortcuts     import render, redirect, get_object_or_404
from  django.http          import HttpResponseRedirect
from  django.urls          import reverse, reverse_lazy
from .models               import Post, Category, Comment
from .forms                import PostCreateForm, CommentCreateForm


def CategoryPosts(request, category):
    category_id = Category.objects.get(name = category.replace('-', ' ')).id
    category_posts = Post.objects.filter(category = category_id)
    return render(request, 'blog/category_posts.html', {'category': category.title().replace('-', ' '), 'category_id' : category_id, 'category_posts' : category_posts})


# def CategoryList(request):
#     category_list = Category.objects.all()
#     return render(request, 'blog/category_list.html', {'category_list' : category_list})


def CategoryList(request):  # list with checkboxes
    category_list = Category.objects.all()
    if request.method == "POST":
        for deleted in request.POST.getlist('delete'):
            Category.objects.filter(id=deleted).delete()
    return render(request, 'blog/category_list.html', {'category_list': category_list})


def LikeView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)
    return HttpResponseRedirect(reverse('post_detail', args=[str(post_id)]))


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    class Meta:
        ordering = ['-date']

    def get_queryset(self):
        ''' flip sort order '''
        if self.request.session.get('sort_order', '-'):
            self.request.session['sort_order'] = ''
        else:
            self.request.session['sort_order'] = '-'
        order = self.request.session['sort_order']

        ''' column to sort - sent from template '''
        column = self.request.GET.get("column")
        if(column): return Post.objects.all().order_by(order+column)
        else: return Post.objects.all()

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     category_list = Category.objects.all()
    #     context['category_list'] = category_list
    #     return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['total_likes'] = post.total_likes()
        context['liked'] = post.likes.filter(id=self.request.user.id).exists()
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreateForm
    success_url = reverse_lazy("post_list")
    template_name = 'blog/comment_create.html'

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     # print("*** context ", context)
    #     # print("*** context['form'] ", context['form'])
    #     print("*** self.kwargs ", self.kwargs)
    #     print("*** self.request ", self.request)
    #     print("*** self.request.GET['comment_id'] ", self.request.GET['comment_id'])
    #     # print("*** self.kwargs['comment_id'] ", self.kwargs['comment_id'])
    #     context['post_pk']    = self.kwargs["post_pk"]
    #     comment_id = self.request.GET['comment_id']
    #     if(comment_id):
    #         context['comment'] = Comment.objects.get(id=comment_id)
    #     return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['post_pk'])
        return super().form_valid(form)

    # def get_queryset(self):
    #     print("*** get_queryset self.kwargs ", self.kwargs)


# class PostDetail(DetailView):
#     model = Post
    # template_name = 'blog/post_detail.html'

def CommentDelete(request, comment_id, post_id):
    Comment.objects.filter(id=comment_id).delete()
    return HttpResponseRedirect(reverse_lazy('post_detail', args=(post_id,)))
