from django.contrib.auth.models import User
from django.db                  import models
from django.urls                import reverse
from ckeditor.fields            import RichTextField
from polls.models               import Bill
from events.models              import Event


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list')


tags = [('media', 'Media'), ('parties', 'Political Parties'), ('democracy', 'Democracy'), ('communism', 'Communism'), ('countries', 'Countries'), ('currencies','Currencies')]

# categories = Category.objects.all().values_list('name', 'name')
# category_list=[]
# for category in categories:
#     category_list.append(category)

class Post(models.Model):
    title     = models.CharField(max_length=255)
    image     = models.ImageField(null=True, blank=True, upload_to="images/blog")
    author    = models.ForeignKey(User,     on_delete=models.CASCADE, null=True, blank=True)
    category  = models.ForeignKey(Category, on_delete=models.SET_NULL, default="", null=True, blank=True)
    bill      = models.ForeignKey(Bill,     on_delete=models.SET_NULL, default="", null=True, blank=True)
    event     = models.ForeignKey(Event,    on_delete=models.SET_NULL, default="", null=True, blank=True)
    # category  = models.CharField(choices=category_list, max_length=64, null=True, blank=True)
    tag       = models.CharField(choices=tags, max_length=64, null=True, blank=True)
    excerpt   = models.CharField(max_length=255, null=True, blank=True)
    body      = RichTextField(blank=True, null=True)
    # body      = models.TextField()
    date      = models.DateField(auto_now_add=True)
    likes     = models.ManyToManyField(User, related_name='post_likes')

    def __str__(self):
        return self.title + ', ' + str(self.author)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post   = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    body   = RichTextField(blank=True, null=True)
    date   = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return '%s - %s' % (str(self.post.title), str(self.author))
    #     # return self.post.title + ', ' + str(self.author)
