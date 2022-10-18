# from  django.shortcuts import render, redirect
# from  django.contrib import messages
# from  users.models import UserExtension
# from  django.http import HttpResponseRedirect
# from .models import *
# import requests
# from django.core.mail import send_mail
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.header import Header
# from email.utils import formataddr
import smtplib
import requests
from django.shortcuts import render, redirect
from django.contrib   import messages
from datetime         import date
from email.message    import EmailMessage
from campaigns.models import Contact
from .models          import Messaging


def GetStreets(zipcode):
    url      = 'https://www.melissa.com/v2/lookups/addresssearch/'
    params   = {'zip':zipcode, 'id':'XPiaSe2P9BN1lYpB5mgP7m**', 'fmt':'json',}
    response = requests.get(url, params=params)
    records  = response.json()['Records']
    streets  = []
    for i in range(len(records)):
        streets.append(records[i]['Street'])
    return streets


def SendEmails(subject, to, bcc, from_name, content):
    user     = 'gu93vusk@gmail.com'
    password = 'dgshtzzdqhevjqda' # app password

    msg = EmailMessage()
    msg['subject']  = subject
    msg['to']       = to
    # msg['bcc']      = ',  '.join(bcc)
    msg['bcc']      = bcc
    msg['from']     = from_name
    # msg['sender']     = sender
    # msg['from_addr'] = 'mailer@democraticempire.com'
    # msg['reply_to']  = reply_to
    msg.set_content(content)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    # server.sendmail(reply_to, bcc, msg.as_string())
    server.send_message(msg) # send_message() is a wrapper for sendmail()
    server.quit


# def MessagingDelete(request):
#     if request.method == 'POST':
#         for deleted in request.POST.getlist('delete'):
#             message = Messaging.objects.get(id=deleted)
#             if message.owner == request.user:
#                 message.delete()
#         messages.info(request, "Messaging deleted")
#     return redirect("messaging_list")


def MessagingList(request):
    # print(' *** request.GET  ', request.GET )
    # print(' *** request.POST ', request.POST )
    column = request.GET.get("column")
    if request.method == 'POST':
        for deleted in request.POST.getlist('delete'):
            message = Messaging.objects.get(id=deleted)
            if message.owner == request.user:
                # print(' *** deleted ', message )
                message.delete()
        messages.info(request, "Messaging deleted")
        messaging = Messaging.objects.all()
    # return redirect("messaging_list")
    elif column: # clicked on column heading to sort
        ''' flip sort order '''
        if request.session.get('sort_order', '-'):
            request.session['sort_order'] = ''
        else:
            request.session['sort_order'] = '-'
        order = request.session['sort_order']

        ''' column to sort - sent from template '''
        if column == 'district':
            messaging = Messaging.objects.filter(district = request.user.userextension.district)
        elif column == 'zipcode':
            messaging = Messaging.objects.filter(zipcode = request.user.userextension.zipcode)
        elif column == 'delete':
            messaging = Messaging.objects.filter(owner = request.user)
        else:
            messaging = Messaging.objects.all().order_by(order+column)
    else: # no column header selected to sort
        messaging = Messaging.objects.all()
    return render(request, "messaging/messaging_list.html",  {'messaging':messaging})


def MessagingEmail(request):
    print(' *** request.GET  ', request.GET )
    print(' *** request.POST ', request.POST )
    if request.method == 'POST':
        form = request.POST
        print(' *** form ', form)

        ### if 'All Streets' button pressed (ie. not selection of individual streets, but all streets in zipcode)
        if form['submit_button'] == 'All Streets':
            return render(request, "messaging/messaging_email.html", {'zipcode':form['zipcode'], 'street':form['submit_button']})

        ### zipcode entered, but street not selected
        elif form['zipcode'] and not form['street']: 
            streets = GetStreets(form['zipcode'])
            return render(request, "messaging/messaging_email.html", {'zipcode':form['zipcode'], 'streets':streets})

        ### street selected (zipcode already selected)
        elif form['street'] and not form['subject']: 
            return render(request, "messaging/messaging_email.html", {'zipcode':form['zipcode'], 'street':form['street']})

        ### post message contect, and send
        elif form['subject']:
            # print(' *** form ', form)
            # print(' *** contacts ', contacts)

            # campaign       = Campaign()
            # campaign.name  = '[Email] '+form['subject']
            # campaign.owner = request.user
            # Campaign.objects.get_or_create(name = campaign.name, owner = campaign.owner)
            # # campaign.save()
            # campaign = Campaign.objects.get(name = campaign.name, owner = campaign.owner)
            # print(' *** campaign ', campaign.name, campaign.owner)

            ### send messages to email addresses on the selected street(s)
            if form['street'] == 'All Streets':
                contacts = Contact.objects.filter(zipcode=form['zipcode']).order_by('email')
            else:
                contacts = Contact.objects.filter(zipcode=form['zipcode'], street=form['street']).order_by('email')
            # print(' *** contacts ordered by email ', contacts)
            bcc = []
            prev_email = ''
            for contact in contacts:
                if contact.email != prev_email:
                    prev_email = contact.email
                    bcc.append(contact.email)
                    # contact.date = date.today()
                    # contact.campaign = campaign
                    # # contact.campaign = Campaign.objects.get(id=form['campaign'])
                    # print(' *** contact ', contact)
                    # contact.save()
            # print(' *** bcc ', bcc)
            SendEmails(
                subject   = form['subject'], 
                to        = request.user.email,
                bcc       = bcc, 
                from_name = form['from_name'],
                content   = form['content'], )
            messages.info(request, 'Message "' + form['subject'] + '" sent to ' + form['zipcode'] + ' ' + form['street'].capitalize())
            
            ### record mailout on database
            messaging = Messaging()
            messaging.subject = form['subject']
            messaging.date    = date.today()
            messaging.owner   = request.user
            messaging.zipcode = form['zipcode']
            messaging.street  = form['street']
            messaging.save()

            return redirect("messaging_list")


            # print(' *** sent to ', request.user.email)
            # prev_email = ''
            # for contact in contacts:
            #     if contact.email != prev_email:
            #         prev_email = contact.email
            #         SendEmails(
            #             subject   = form['subject'], 
            #             to        = contact.email, 
            #             # bcc       = bcc, 
            #             from_name = form['from_name'],
            #             reply_to  = form['reply_to'],
            #             content   = form['content'], )
            #         print(' *** sent to ', contact.email)
    # else: messages.info(request, "Please enter ZIP code")

    return render(request, "messaging/messaging_email.html", {})

