# from django.db.models import CharField, Value
from  django.shortcuts import render, redirect
from  django.contrib import messages
from  users.models import UserExtension
from  django.http import HttpResponseRedirect
from .models import *
import requests


def CampaignContactsList(request):
    # print(' *** request.GET  ', request.GET )
    # print(' *** request.POST ', request.POST )
    column = request.GET.get("column")
    if request.method == 'POST':
        for deleted in request.POST.getlist('delete'):
            contact = Contact.objects.get(id=deleted)
            if contact.owner == request.user:
                # print(' *** deleted ', contact )
                contact.delete()
        messages.info(request, "Contact deleted")
        contacts = Contact.objects.all()

    elif column: # clicked on column heading to sort
        ''' flip sort order '''
        if request.session.get('sort_order', '-'):
            request.session['sort_order'] = ''
        else:
            request.session['sort_order'] = '-'
        order = request.session['sort_order']

        ''' column to sort - sent from template '''
        if column == 'number':
            contacts = Contact.objects.all().order_by(order+'street', order+'number', )
        elif column == 'district':
            contacts = Contact.objects.filter(district = request.user.userextension.district)
        elif column == 'zipcode':
            contacts = Contact.objects.filter(zipcode = request.user.userextension.zipcode)
        elif column == 'delete':
            contacts = Contact.objects.filter(owner = request.user)
        else:
            contacts = Contact.objects.all().order_by(order+column)
    else: # no column header selected to sort
        contacts = Contact.objects.all()

    return render(request, "campaigns/campaign_contacts_list.html", {'contacts':contacts})
    

def CampaignContactsDelete(request):
    if request.method == 'POST':
        for deleted in request.POST.getlist('delete'):
            contact = Contact.objects.get(id=deleted)
            if contact.owner == request.user:
                contact.delete()
        messages.info(request, "Contact deleted")
        # back = request.POST.get('back', '/')
        # return HttpResponseRedirect(back)
        return HttpResponseRedirect('/campaigns/campaign_contacts')
    return render(request, "myvote/home.html", {})


def CampaignContactsCreate(request):
    zipcode = request.GET.get("zipcode", None)
    street  = request.GET.get("street",  None)
    number  = request.GET.get("number",  None)
    # request.session['zipcode'] = zipcode
    # request.session['street']  = street
    # request.session['number']  = number
    if request.method == 'POST':
        # zipcode = request.session.get('zipcode', None)
        # street  = request.session.get('street',  None)
        # number  = request.session.get('number',  None)
        form = request.POST
        # print(' *** address ', zipcode, street, number)
        # print(' *** form ', form)
        # print(" *** form['campaign'] ", form['campaign'])
        # print(" *** type(form['campaign']) ", type(form['campaign']))
        # print(" *** request.POST.get('campaign')) ", request.POST.get('campaign'))
        contact = Contact()
        contact.zipcode  = form['zipcode']
        contact.street   = form['street']
        contact.number   = form['number']
        contact.name     = form['name']
        contact.cell     = form['cell']
        contact.email    = form['email']
        contact.date     = form['date']
        contact.campaign = Campaign.objects.get(id=form['campaign'])
        contact.owner    = request.user
        contact.save()
        messages.info(request, "Contact saved : " + contact.name)
        # contacts = Contact.objects.all()
        contacts = Contact.objects.filter( zipcode = form['zipcode'], street = form['street'], number = form['number'], )
        context  = {'zipcode':form['zipcode'], 'street':form['street'], 'number':form['number'], 'contacts':contacts, }
        return render(request, "campaigns/campaign_contacts_address.html", context)
    campaigns = Campaign.objects.all()
    return render(request, "campaigns/campaign_contacts_create.html", {'zipcode':zipcode, 'street':street, 'number':number, 'campaigns':campaigns, })


def CampaignContacts(request):
    if request.method == "POST":
        number = request.POST.get('number', None)
        street = request.POST.get('street', None)
        number_prev = request.session.get('number', None)
        street_prev = request.session.get('street', None)
        zipcode = request.user.userextension.zipcode
        # number_prev = request.session.get('number', None)
        # number_prev = request.session.get('number', None)
        # print(' *** number ', number)
        # print(' *** street ', street)
        # print(' *** number_prev ', number_prev)
        # print(' *** street_prev ', street_prev)
        if number: 
            ''' contact details  '''
            request.session['number'] = number
            street   = request.session.get('street', None)
            contacts = Contact.objects.filter(zipcode = zipcode, street  = street, number  = number, )
            # print(' **** number ', number)
            # print(' **** street ', street)
            # print(' **** zipcode ', zipcode)
            # print(' **** contacts ', contacts)        

            ### if not previous contact, do directly to contact form ([Add] button)
            if not contacts: 
                campaigns = Campaign.objects.all()
                context   = {'zipcode':zipcode, 'street':street, 'number':number, 'campaigns':campaigns, }
                return render(request, "campaigns/campaign_contacts_create.html", context)
            else:
                context = {'zipcode':zipcode, 'street':street, 'number':number, 'contacts':contacts, }
                return render(request, "campaigns/campaign_contacts_address.html", context)
        else:
            ''' download list of street numbers for street selected '''
            street  = request.POST['street']
            numbers = request.session.get('numbers', None)
            if not numbers or street != street_prev: # if a new street is selected, get new numbers
                url    = 'https://www.melissa.com/v2/lookups/addresssearch/'
                params = {
                    'zip':request.user.userextension.zipcode, 
                    'id':'XPiaSe2P9BN1lYpB5mgP7m**', 
                    'fmt':'json', 
                    'street':street, }
                response = requests.get(url, params=params)
                records  = response.json()['Records']
                numbers  = []
                for i in range(len(records)):
                    numbers.append(records[i]['Number'])
                # street = records[0]['Street']
                request.session['street']  = street
                request.session['numbers'] = numbers
            context ={'streets':'', 'street':street, 'number':'', 'numbers':numbers, }

    else:
        ''' download list of streets for my zipcode '''
        streets = request.session.get('streets', None)
        if not streets:
            # print(' *** streets from session memory ')
            url      = 'https://www.melissa.com/v2/lookups/addresssearch/'
            params   = {'zip':request.user.userextension.zipcode, 'id':'XPiaSe2P9BN1lYpB5mgP7m**', 'fmt':'json',}
            response = requests.get(url, params=params)
            records  = response.json()['Records']
            streets  = []
            for i in range(len(records)):
                streets.append(records[i]['Street'])
            request.session['streets'] = streets
        context ={'streets':streets, 'street':'', 'number':'', 'numbers':'', }

    return render(request, "campaigns/campaign_contacts.html", context)


    # url = 'https://api.propublica.org/congress/v1/bills/search.json?sort=date&dir=desc'
    # headers = {'X-API-Key': 'yh0XpOTmFdd8SRfOHu2fCNNnAXbXp4jC52zeSLdV'}
    # api_request = requests.get(url, headers = headers)
    # bills = api_request.json()['results'][0]['bills']

    # if request.method == "POST":
    #     form = request.POST
    #     if (Role.objects.filter(owner = request.user.id, name = form['role'])):
    #         messages.warning(request, "Sorry, the role already exists : " + form['role'])
    #     else:
    #         role = Role()
    #         role.name  = form['role']
    #         role.owner = request.user
    #         role.save()
    #     return redirect("team_define_roles")


def CampaignCreate(request):
    if request.method == "POST":
        form = request.POST
        if (Campaign.objects.filter(owner = request.user.id, name = form['campaign'])):
            messages.warning(request, "Sorry, the campaign already exists : " + form['campaign'])
        else:
            campaign = Campaign()
            campaign.name  = form['campaign']
            campaign.owner = request.user
            campaign.save()
        return redirect("campaign_define")
    return render(request, "campaigns/campaign_create.html", {})

# class TeamCreateRole(CreateView):
#     model         = Role
#     template_name = 'users/team_create_role.html'
#     success_url   = reverse_lazy('team_define_roles')
#     fields        = ('name', 'owner', )


def CampaignDefine(request):  # list with checkboxes
    campaign_list = Campaign.objects.all()
    if request.method == "POST":
        for deleted in request.POST.getlist('delete'):
            compaign_delete = Campaign.objects.get(id=deleted)
            if (compaign_delete.owner != request.user): 
                messages.warning(request, "Sorry, only the owner can delete a role: " + str(compaign_delete.owner))
            elif (UserExtension.objects.filter(role=compaign_delete)):
                messages.warning(request, "Sorry, the role has been assigned")
            else:
                compaign_delete.delete()
    return render(request, 'campaigns/campaign_define.html', {'campaign_list': campaign_list, })
