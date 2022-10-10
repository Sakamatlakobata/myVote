# from  django.contrib import admin
from  django.urls    import path
from .views          import district_zipcode

# admin.site.site_header = 'myVote'
# admin.site.index_title = 'myVote'
# admin.site.site_title  = 'myVote'

urlpatterns = [
    path('district_zipcode', district_zipcode, name='district_zipcode'),
    # path('district_display', district_display, name='district_display'),
]
