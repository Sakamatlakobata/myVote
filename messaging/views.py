# from  django.shortcuts import render, redirect
# from  django.contrib import messages
# from  users.models import UserExtension
# from  django.http import HttpResponseRedirect
# from .models import *
# import requests
from django.shortcuts import render
import smtplib, ssl
from email.message import EmailMessage
from django.core.mail import send_mail


def email_send(subject, body, to, sender):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to']      = to
    msg['from']    = sender

    user     = 'fouriewa@gmail.com'
    password = 'igclotkpqvapkcnt' # app password

    # service = smtplib.SMTP_SSL('smtp.gmail.com', 587, context=ssl.create_default_context())
    # print(' *** service', service)
    # service = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
    # service.login(user, password)
    # result = service.sendmail('fouriewa@gmail.com', 'fouriewa-subscription@yahoo.com', f"Subject: {'subject'}\n{'content'}")
    # service.quit()

    server = smtplib.SMTP('smtp.gmail.com', 465)
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    print(' *** server', server)
    # server.starttls()
    # # server.startssl()
    # server.login(user, password)
    # # server.send_message(msg)
    # server.sendmail(msg)
    # server.quit


def MessagingList(request):
    return render(request, "messaging/messaging_list.html",  {})


def MessagingEmail(request):
    print(' *** MessagingEmail called')
    # smtp_message = email_send('Test gmail SMTP', 'This is the body and stuff', 'fouriewa-subscription@yahoo.com', 'fouriewa@gmail.com', )
    # print(' *** smtp_message ', smtp_message)

    send_mail(
        'Subject line',
        'Message body',
        'fouriewa@gmail.com',
        ['fouriewa-subscription@yahoo.com'],   
        fail_silently=False,     
    )
    print(' *** Mail sent')

    return render(request, "messaging/messaging_email.html", {})


def MessagingSMS(request):
    return render(request, "messaging/messaging_sms.html",   {})
