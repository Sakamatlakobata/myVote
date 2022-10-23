# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from  django.contrib.auth.forms import PasswordChangeForm
# from  django.views import generic
# from  django.views.generic import UpdateView, DetailView, CreateView, ListView
# from  django.contrib.auth import login
# from  django.shortcuts import render, redirect, get_object_or_404
from  django.contrib.auth.views import PasswordChangeView
from  django.views.generic import CreateView
from  django.shortcuts import render, redirect
from  django.contrib import messages
from  django.urls import reverse_lazy
from .forms  import UsersPasswordForm
from .models import User, UserExtension, Role


def TeamAddMembers(request):
    if request.method == "POST":
        # print('*** post', request.POST)
        # if (column):
        #     print('*** column ', column)
        if (request.POST.get("button", None) == 'Save'):
            # print('*** request.POST.get("button", None) ', request.POST.get("button", None))
            roles = request.POST.getlist('roles', None)
            for role in roles:
                role = role.split(",")
                userextension = UserExtension.objects.get(user=User.objects.get(id=role[0]))
                userextension.role = Role.objects.get(name=role[1])
                userextension.save()
            messages.info(request, "Members roles updated")
        users = User.objects.all().exclude(userextension__role__name = "-")
        return render(request, "users/team_list_members.html", {'users':users})
    else:
        column = request.GET.get("column")
        if (column):
            ''' flip sort order '''
            if request.session.get('sort_order', '-'):
                request.session['sort_order'] = ''
            else:
                request.session['sort_order'] = '-'
            order = request.session['sort_order']

            ''' column to sort - sent from template '''
            # print('*** column ', column)
            if (column == 'district'):
                users = User.objects.filter(userextension__district = request.user.userextension.district)
            elif (column == 'zipcode'):
                users = User.objects.filter(userextension__zipcode = request.user.userextension.zipcode)
            else:
                users = User.objects.all().order_by(order+column)
        else:
            users = User.objects.all()
        roles = Role.objects.all()

    return render(request, "users/team_add_members.html", {'users':users, 'roles':roles})


def TeamListMembers(request):
    column = request.GET.get("column")
    if request.method == 'POST':
        # print(' *** request.POST ', request.POST)
        no_role = Role.objects.get(name = '-')
        # print(' *** no_role ', no_role )
        for deleted in request.POST.getlist('delete'):
            user = User.objects.get(id=deleted)
            if user.userextension.role.owner == request.user:
                # print(' *** deleted ', user.username )
                userextension = UserExtension.objects.get(user = user)
                userextension.role = no_role
                userextension.save()
                # print(' *** userextension ', userextension )
                # user.delete()
        messages.info(request, "Team member deleted")
        users = User.objects.all().exclude(userextension__role__name = "-")

    ### if column heading selected to sort on
    if (column):
        ''' flip sort order '''
        if request.session.get('sort_order', '-'):
            request.session['sort_order'] = ''
        else:
            request.session['sort_order'] = '-'
        order = request.session['sort_order']

        ''' column to sort - sent from template '''
        if (column == 'district'):
            users = User.objects.filter(userextension__district = request.user.userextension.district).exclude(userextension__role__name = "-")
        elif (column == 'zipcode'):
            users = User.objects.filter(userextension__zipcode = request.user.userextension.zipcode).exclude(userextension__role__name = "-")
        elif column == 'delete':
            roles = UserExtension.objects.values_list('role__name', 'role__owner')
            # print(' *** roles ', roles)
            # print(' *** request.user ', request.user.id, request.user)
            # print(' *** userextension__role__owner ', request.user.userextension.role)
            users = User.objects.filter(userextension__role__owner = request.user)
        elif (column == 'role'):
            users = User.objects.all().exclude(userextension__role__name = "-").order_by(order+'userextension__role__name')
        else:
            users = User.objects.all().exclude(userextension__role__name = "-").order_by(order+column)
    else:
        users = User.objects.all().exclude(userextension__role__name = "-")
    return render(request, "users/team_list_members.html", {"users":users})


def TeamCreateRole(request):
    if request.method == "POST":
        form = request.POST
        if (Role.objects.filter(owner = request.user.id, name = form['role'])):
            messages.warning(request, "Sorry, the role already exists : " + form['role'])
        else:
            role = Role()
            role.name  = form['role']
            role.owner = request.user
            role.save()
        return redirect("team_define_roles")
    return render(request, "users/team_create_role.html", {})

# class TeamCreateRole(CreateView):
#     model         = Role
#     template_name = 'users/team_create_role.html'
#     success_url   = reverse_lazy('team_define_roles')
#     fields        = ('name', 'owner', )


def TeamDefineRoles(request):  # list with checkboxes
    role_list = Role.objects.all().exclude(name = "-")
    if request.method == "POST":
        for deleted in request.POST.getlist('delete'):
            role_delete = Role.objects.get(id=deleted)
            if (role_delete.owner != request.user): 
                messages.warning(request, "Sorry, only the owner can delete a role: " + str(role_delete.owner))
            elif (UserExtension.objects.filter(role=role_delete)):
                messages.warning(request, "Sorry, the role has been assigned")
            else:
                role_delete.delete()
    return render(request, 'users/team_define_roles.html', {'role_list': role_list, })


def UsersRegistrationView(request, *args, **kwargs):
    # user = User.objects.get(id=request.user.id)
    # userextension = UserExtension.objects.get(user=user)
    if request.method == "POST":
        form = request.POST
        # print('*** form ', form)
        if form['password'] != form['password2']:
            messages.warning(request, "The passwords don't match, sorry")
            # return render(request, "users/users_register.html", {})
            return redirect("users_register")
        new_user = User.objects.create_user(
            username   = form['username'],
            first_name = form['first_name'],
            last_name  = form['last_name'],
            email      = form['email'],
            password   = form['password'],)
        new_extension = UserExtension(
            user    = new_user,
            cell    = form['cell'],
            zipcode = form['zipcode'],)
        new_extension.save()
        messages.success(request, "Account " + form['username'] + " created")
        return redirect("users_login")
    # context= {'user':user,'userextension':userextension}
    return render(request, "users/users_register.html", {})


# def UsersRegistrationView(request):
#     if request.method == "POST":
#         form = UsersRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful." )
#             return redirect("users_login")
# 			# return redirect("main:homepage")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
# 	# form = UsersRegistrationForm()
#     context = {
#         "register_form":UsersRegistrationForm(),
#         "userextension":UsersExtensionRegistrationForm(),}
#     return render (request=request, template_name="users/users_register.html", context=context)


def UsersDetail(request, pk):
    user = User.objects.get(id=pk)
    userextension = UserExtension.objects.get(user=user)
    context= {'user':user,'userextension':userextension}
    return render(request, "users/users_detail.html", context)


def UsersEditView(request):
    user = User.objects.get(id=request.user.id)
    userextension = UserExtension.objects.get(user=user)
    if request.method == "POST":
        form = request.POST
        user.username         = form['username']
        user.first_name       = form['first_name']
        user.last_name        = form['last_name']
        user.email            = form['email']
        user.save()
        userextension.zipcode = form['zipcode']
        userextension.cell    = form['cell']
        userextension.user    = user
        userextension.save()
        messages.success(request, "Account updated")
    context= {'user':user,'userextension':userextension}
    return render(request, "users/users_edit.html", context)

    # def post(self, request, **kwargs):
    #     event = Event.objects.get(id=kwargs['pk'])
    #     if self.request.user in event.attendees.all():
    #         event.attendees.remove(self.request.user)
    #     else:
    #         event.attendees.add(self.request.user)
    #     messages.success(self.request, "Account updated")
    #     return HttpResponseRedirect(reverse('event_detail', args=[str(self.kwargs['pk'])]))
            # userextension = UserExtension.objects.get(user=self.request.user)


class UsersPasswordView(PasswordChangeView):
    form_class    =  UsersPasswordForm
    # form_class    =  PasswordChangeForm
    template_name = 'users/users_password.html'
    success_url   =  reverse_lazy('post_login')


# class UserRegisterView(generic.CreateView):
#     form_class    = UserCreationForm
#     template_name = 'users/register.html'
#     success_url   = reverse_lazy('users_login')


# class UsersProfileView(DetailView):
#     model = UserExtension
#     template_name = 'users/users_profile.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data()
#         user_profile = get_object_or_404(UserExtension, id=self.kwargs['pk'])
#         # print('user_profile:', user_profile)
#         context['user_profile'] = user_profile
#         return context


# class UsersPageEditView(UpdateView):
#     model         = UserExtension
#     fields        = ['bio', 'website', 'facebook', 'twitter', 'image']
#     template_name = 'users/users_page_edit.html'
#     success_url   =  reverse_lazy('post_list')


# class UsersPageCreateView(CreateView):
#     model         = UserExtension
#     template_name = 'users/users_page_create.html'
#     fields        = ['bio', 'website', 'facebook', 'twitter', 'image']
#     success_url   =  reverse_lazy('post_list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# class UsersEditView(UpdateView):
#     model         = UserExtension
#     fields        = ['user.username', 'user.first_name', 'user.last_name', 'user.email', 'userextension.zipcode', 'user.last_login', 'user.date_joined']
#     template_name = 'users/users_edit.html'
#     success_url   =  reverse_lazy('post_list')

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data()
#         try:
#             userextension = UserExtension.objects.get(user=self.request.user)
#         except:
#             context['userextension'] = ""
#         else:
#             context['userextension'] = userextension
#         return context

#     def get_object(self):
#         return self.request.user

# class UsersDetail(DetailView):
#     model = UserExtension
#     fields = ['user.username', 'user.first_name', 'user.last_name', 'user.email', 'userextension.cell', 'userextension.zipcode']
#     template_name = 'users/users_detail.html'


