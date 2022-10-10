# from django.template.defaulttags import register
from  django.views.generic import ListView, FormView, UpdateView
from  django.shortcuts     import render, get_object_or_404
from  django.contrib       import messages
from  django.http          import HttpResponse, HttpResponseRedirect
from  django.urls          import reverse
from  district.utilities   import get_bills
from .models               import Bill, Poll, VOTE_TYPES


def PollsNewBills(request):  # list with checkboxes
    new_bills_list = get_bills()
    if request.method == "POST":
        for bill in request.POST.getlist('add'):
            if(not Bill.objects.filter(bill_id=bill).exists()):
                detail = [element for element in new_bills_list if element['bill_id']==bill]
                # print('*** detail ', detail[0]['bill_id'], detail[0]['introduced_date'])
                Bill.objects.create(
                    bill_id = detail[0]['bill_id'],
                    type    = detail[0]['bill_type'],
                    number  = detail[0]['number'],
                    text    = detail[0]['short_title'],
                    url     = detail[0]['congressdotgov_url'],
                    date_introduced = detail[0]['introduced_date'],)
        messages.info(request, "New bills added")
        bills_list = Bill.objects.order_by('-date_introduced')
        return render(request, 'polls/polls_list.html', {'bills_list': bills_list})
    return render(request, 'polls/polls_new_bills.html', {'new_bills_list': new_bills_list})


class PollsRecord(ListView):
    model = Poll
    template_name = 'polls/polls_record.html'

    def get_context_data(self,**kwargs):
        context = super(PollsRecord,self).get_context_data(**kwargs)
        context['polls_list'] = Poll.objects.filter(user=self.request.user.id).order_by('-bill')
        return context


def PollsList(request):
    if request.method == "POST":
        for deleted in request.POST.getlist('delete'):
            bill = Bill.objects.filter(bill_id=deleted)[0]
            if(not Poll.objects.filter(bill=bill)): # check that there is no voting record
                bill.delete()
        messages.info(request, "Bills deleted")
    bills_list = Bill.objects.order_by('-date_introduced')

    ''' sort columns '''
    column = request.GET.get("column")
    if(column):
        if request.session.get('sort_order', '-'): request.session['sort_order'] = ''
        else: request.session['sort_order'] = '-'
        order = request.session['sort_order']
        bills_list = Bill.objects.all().order_by(order+column)

    return render(request, 'polls/polls_list.html', {'bills_list': bills_list})


# class PollsList(ListView):
#     template_name = 'polls/polls_list.html'
#     context_object_name = 'latest_bills_list'

#     def get_queryset(self):
#         return Bill.objects.order_by('-date_introduced')
    

def PollsResult(request, bill_id):
    try:    bill = Bill.objects.get(pk=bill_id)
    except: bill = ""

    ''' count the votes per choice for this bill '''
    polls = Poll.objects.filter(bill = bill)
    votes = {}
    if (polls):
        for key, value in VOTE_TYPES:
            votes[value] = polls.filter(vote=key).count()

    context = {}
    context['bill_type']   = bill.type
    context['bill_number'] = bill.number
    context['bill_text']   = bill.text
    context['votes']       = votes

    return render(request, 'polls/polls_result.html', context)


def PollsVote(request, bill_id):
    try:    bill = Bill.objects.get(pk=bill_id)
    except: bill = ""

    if (not request.POST):
        # print('*** user ', request.user)
        # print('*** vote ', Poll.objects.get(bill=bill, user=request.user).vote)
        vote = Poll.objects.filter(bill=bill, user=request.user)
        if(vote): vote = vote[0].vote
        else: vote = ''
        # if(vote): print('*** vote found ', vote[0].vote)
        return render(request, 'polls/polls_vote.html', {'bill': bill, 'vote': vote, 'VOTE_TYPES': VOTE_TYPES, 'error_message': 'Please make a choice'})
        # return render(request, 'polls/polls_vote.html', {'bill': bill, 'VOTE_TYPES': VOTE_TYPES, 'error_message': 'Please make a choice'})
    else:
        try:
            vote = request.POST['vote']
        except:
            messages.warning(request, "Please make a choice")
            return HttpResponseRedirect(reverse('polls_vote', args=(bill.id,)))
        else:
            poll = Poll.objects.filter(bill=bill, user=request.user)
            if (not poll):
                Poll.objects.create(
                    bill = bill,
                    vote = vote,
                    # vote = request.POST['vote'],
                    user = request.user,
                )
            else: # change previous vote
                poll = Poll.objects.get(bill=bill, user=request.user)
                poll.vote = vote
                # poll.vote = request.POST['vote']
                poll.save()
            return HttpResponseRedirect(reverse('polls_result', args=(bill.id,)))
