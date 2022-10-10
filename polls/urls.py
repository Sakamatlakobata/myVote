# from  django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from  django.contrib.auth.views import LoginView, PasswordChangeView
# from  django.views import generic
# from  django.urls  import reverse_lazy
# from .forms        import UsersRegistrationForm, UsersPasswordForm
from  django.urls import path
from .views       import PollsList, PollsResult, PollsVote, PollsRecord, PollsNewBills  

urlpatterns = [
    path('polls_list',                 PollsList,               name='polls_list'),
    path('polls_record',               PollsRecord.as_view(),   name='polls_record'),
    path('polls_new_bills',            PollsNewBills,           name='polls_new_bills'),
    path('polls_result/<int:bill_id>', PollsResult,             name='polls_result'),
    path('polls_vote/<int:bill_id>',   PollsVote,               name='polls_vote'),
    # path('polls_detail/<int:bill_id>', PollsDetail, name='polls_detail'),
    # path('users_page_edit/<int:pk>', UsersPageEditView.as_view(), name='users_page_edit'),
]
