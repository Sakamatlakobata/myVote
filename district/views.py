# from accounts.models  import Account
# from myvote.utilities import json_extract
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.models import User
from django.http      import HttpResponse
from django.shortcuts import render, redirect
from users.models     import UserExtension
from .forms           import GetZIPcode
# from .models          import Account
from .utilities       import json_extract
from django.contrib   import messages
import requests


def get_member(ZIPcode):
    endpoint = "https://api.geocod.io/v1.7/geocode"
    params = {  'api_key':'b12b4b2046b214a066a2363130b422b63a26222',
                'fields':'cd', # congressional district
                'q':ZIPcode,}
                # 'q':form.cleaned_data['ZIPcode'],}
    response = requests.get(endpoint, params=params)
    # print('length of response', len(response.text), '[', response.text, ']')
    if response.text.find('error') > 0:
        context = response.json()
    else:
        last_name       = json_extract(response.json(),'last_name'      )[0] # 0 = congress, 1,2 = senators
        first_name      = json_extract(response.json(),'first_name'     )[0]
        congress_id     = json_extract(response.json(),'bioguide_id'    )[0] # bioguide = congress
        govtrack_id     = json_extract(response.json(),'govtrack_id'    )[0] 
        thomas_id       = json_extract(response.json(),'thomas_id'      )[0]
        opensecrets_id  = json_extract(response.json(),'opensecrets_id' )[0]
        votesmart_id    = json_extract(response.json(),'votesmart_id'   )[0]
        icpsr_id        = json_extract(response.json(),'icpsr_id'       )[0]
        phone           = json_extract(response.json(),'phone'          )[0]
        district        = json_extract(response.json(),'name'           )[0]
        district_number = json_extract(response.json(),'district_number')[0]
        congress_url    = 'https://www.congress.gov/member/member/'    + congress_id
        govtrack_url    = 'https://www.govtrack.us/congress/members/'  + govtrack_id
        opensecrets_url = 'https://www.opensecrets.org/search?q='      + opensecrets_id
        votesmart_url   = 'https://justfacts.votesmart.org/candidate/' + votesmart_id
        icpsr_url       = 'https://voteview.com/person/'               + icpsr_id
        context = { 'last_name'       :last_name,
                    'first_name'      :first_name,
                    'congress_id'     :congress_id,
                    'congress_url'    :congress_url,
                    'govtrack_id'     :govtrack_id,
                    'govtrack_url'    :govtrack_url,
                    'thomas_id'       :thomas_id,
                    'opensecrets_id'  :opensecrets_id,
                    'opensecrets_url' :opensecrets_url,
                    'votesmart_id'    :votesmart_id,
                    'votesmart_url'   :votesmart_url,
                    'icpsr_id'        :icpsr_id,
                    'icpsr_url'       :icpsr_url,
                    'phone'           :phone,
                    'ZIPcode'         :ZIPcode,
                    'district_number' :district_number,
                    'district'        :district,}
                    # 'ZIPcode'        :form.cleaned_data['ZIPcode'],}
        # print(district, district_number)
    return context


# views functions
# return member of congress for ZIPcode
def district_zipcode(request):
    if request.method == "POST":
        form = GetZIPcode(request.POST)
        if form.is_valid():
            context = get_member(form.cleaned_data['ZIPcode'])
            if 'error' in context:
                messages.warning(request, context['error'] + ' ZIPcode entered: ' + form.cleaned_data['ZIPcode'])
            return render(request, 'district/district_display.html', context)

    if request.user.is_authenticated: 
        try:
            zipcode = UserExtension.objects.filter(user=request.user)[0].zipcode
        except:
            return render(request, 'district/district_zipcode.html', {'form':GetZIPcode()})
        context = get_member(zipcode)
        context['description']='This is your electoral district for ZIPcode '+zipcode
        return render(request, 'district/district_display.html', context)

    return render(request, 'district/district_zipcode.html', {'form':GetZIPcode()})


# @login_required(login_url='/accounts/login/', redirect_field_name='district/district_login')
@login_required(login_url='/accounts/login/')
def district_login(request):

    if request.user.is_authenticated: # if logged in get ZIPcode from account
        zipcode = User.objects.filter(user=request.user)[0].zipcode
        # zipcode = Account.objects.filter(user=request.user)[0].zipcode
        context = get_member(zipcode)
        return render(request, 'district/district_display.html', context)

    return render(request, 'district/district_login.html', {'form':GetZIPcode()})


def district_display(request):
    return HttpResponse(request)
