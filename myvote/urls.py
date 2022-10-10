from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls    import path, include
from django.conf    import settings
from blog.views     import PostList

# admin.site.site_header = 'myVote'
# admin.site.index_title = 'Admin Page'
# # admin.site.index_title = include("blog/navbar.html")
# admin.site.site_title  = 'myVote5'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('blog/',      include('blog.urls')),
    path('polls/',     include('polls.urls')),
    path('events/',    include('events.urls')),
    path('district/',  include('district.urls')),
    path('users/',     include('django.contrib.auth.urls')),
    path('users/',     include('users.urls')),
    path('campaigns/', include('campaigns.urls')),

    # path('', PostList.as_view()),
    path('', TemplateView.as_view(template_name='myvote/homepage.html')),
    path('home', TemplateView.as_view(template_name='myvote/homepage.html')),
    path('home_page', TemplateView.as_view(template_name='myvote/homepage.html')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
