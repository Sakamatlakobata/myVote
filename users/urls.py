# from  django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .views        import UsersPasswordView, UsersEditView, UsersDetail, UsersRegistrationView
from  django.contrib.auth.views import LoginView, PasswordChangeView
from  django.urls  import path
from  django.views import generic
from  django.urls  import reverse_lazy
from .forms        import UsersPasswordForm
from .views        import *


urlpatterns = [

    path('users_register', UsersRegistrationView, name='users_register'),
    # path('users_register', generic.CreateView.as_view(
    #     form_class    = UsersRegistrationForm,
    #     # form_class    = UserCreationForm,
    #     template_name = 'users/users_register.html',
    #     success_url   = reverse_lazy('users_login'),
    # ), name='users_register'),

    path('users_login', LoginView.as_view(
        template_name = 'users/users_login.html',
    ),  name='users_login'),
    # settings.LOGIN_REDIRECT_URL = "blog/polls_list",
    # default login path in django.contrib.auth.urls is registration/login.htm

    path('users_edit', UsersEditView, name='users_edit'),
    path('users_detail/<int:pk>', UsersDetail, name='users_detail'),
    # path('users_edit', generic.CreateView.as_view(
    #     form_class    = UserChangeForm,
    #     template_name = 'users/users_edit.html',
    #     success_url   = reverse_lazy('post_list'),
    # ), name='users_edit'),

    path('users_password', UsersPasswordView.as_view(), name='users_password'),
    # path('users_password', PasswordChangeView.as_view(template_name='users/users_password.html'), name='users_password'),

    # path('users_profile/<int:pk>', UsersProfileView.as_view(), name='users_profile'),

    # path('users_page_edit/<int:pk>', UsersPageEditView.as_view(), name='users_page_edit'),

    # path('users_page_create', UsersPageCreateView.as_view(), name='users_page_create'),


#  class UserEditView(generic.CreateView):
#     form_class    = UserChangeForm
#     template_name = 'users/user_edit.html'
#     success_url   = reverse_lazy('post_list')

    path('team_add_members',  TeamAddMembers,  name='team_add_members'),
    path('team_list_members', TeamListMembers, name='team_list_members'),
    # path('team_assign_role',  TeamAssignRole,  name='team_assign_role'),
    path('team_define_roles', TeamDefineRoles, name='team_define_roles'),
    path('team_create_role',  TeamCreateRole,  name='team_create_role'),    
    # path('team_create_role', CreateView.as_view( 
    #     model         = Role,
    #     template_name = 'users/team_create_role.html',
    #     success_url   = reverse_lazy('team_define_roles'),
    #     fields        = ('name',)
    # ), name='team_create_role'),

]
