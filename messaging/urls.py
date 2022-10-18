from  django.urls import path
from .views import *

urlpatterns = [

    path('messaging_list',  MessagingList,  name='messaging_list'),
    path('messaging_email', MessagingEmail, name='messaging_email'),

]
