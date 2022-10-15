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
from django.shortcuts import render
from django.contrib   import messages
from email.message    import EmailMessage
from campaigns.models import Campaign, Contact
from datetime         import date


def GetStreets(zipcode):
    url      = 'https://www.melissa.com/v2/lookups/addresssearch/'
    params   = {'zip':zipcode, 'id':'XPiaSe2P9BN1lYpB5mgP7m**', 'fmt':'json',}
    response = requests.get(url, params=params)
    records  = response.json()['Records']
    streets  = []
    for i in range(len(records)):
        streets.append(records[i]['Street'])
    return streets


def SendEmails(subject, to, bcc, reply_to, from_name, content):
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
    msg['reply_to']  = reply_to
    msg.set_content(content)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    # server.sendmail(reply_to, bcc, msg.as_string())
    server.send_message(msg) # send_message() is a wrapper for sendmail()
    server.quit


def MessagingList(request):
    return render(request, "messaging/messaging_list.html",  {})


def MessagingSMS(request):
    return render(request, "messaging/messaging_sms.html",   {})


def MessagingEmail(request):
    if request.method == 'POST':
        form = request.POST
        print(' *** form ', form)

        ### zipcode entered, but street not selected
        if form['zipcode'] and not form['street']: 
            streets = GetStreets(form['zipcode'])
            return render(request, "messaging/messaging_email.html", {'zipcode':form['zipcode'], 'streets':streets})

        ### street selected (zipcode already selected)
        elif form['street'] and not form['subject']: 
            return render(request, "messaging/messaging_email.html", {'zipcode':form['zipcode'], 'street':form['street']})

        ### post message contect, and send
        elif form['subject']:
            contacts = Contact.objects.filter(zipcode=form['zipcode'], street=form['street'])
            print(' *** form ', form)
            print(' *** contacts ', contacts)

            campaign       = Campaign()
            campaign.name  = '[Email] '+form['subject']
            campaign.owner = request.user
            Campaign.objects.get_or_create(name = campaign.name, owner = campaign.owner)
            # campaign.save()
            campaign = Campaign.objects.get(name = campaign.name, owner = campaign.owner)
            print(' *** campaign ', campaign.name, campaign.owner)

            bcc = []
            prev_email = ''
            for contact in contacts:
                if contact.email != prev_email:
                    prev_email = contact.email
                    bcc.append(contact.email)
                    contact.date = date.today()
                    contact.campaign = campaign
                    # contact.campaign = Campaign.objects.get(id=form['campaign'])
                    print(' *** contact ', contact)
                    contact.save()
            SendEmails(
                subject   = form['subject'], 
                to        = request.user.email,
                bcc       = bcc, 
                from_name = form['from_name'],
                reply_to  = form['reply_to'],
                content   = form['content'], )
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
            messages.info(request, 'Message "' + form['subject'] + '" sent to ' + form['zipcode'] + ' ' + form['street'].capitalize())
    else: messages.info(request, "Please enter ZIP code")

    return render(request, "messaging/messaging_email.html", {})

