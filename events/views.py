import datetime
from  django.views.generic import ListView, CreateView, UpdateView, DetailView
from  django.http import HttpResponseRedirect
from  django.shortcuts import render
from  django.urls import reverse
from  django.contrib import messages
from .models import Venue, Event
# from users.models import UserExtension


class EventList(ListView):
    model = Event
    template_name = 'events/event_list.html'
    ordering = ['date']

    def get_queryset(self, *args, **kwargs):
        ''' delete past events '''
        Event.objects.filter(date__lt = datetime.date.today()).delete()

        ''' flip sort order '''
        if self.request.session.get('sort_order', '-'):
            self.request.session['sort_order'] = ''
        else:
            self.request.session['sort_order'] = '-'
        order = self.request.session['sort_order']

        ''' column to sort - sent from template '''
        column = self.request.GET.get("column")

        if( self.request.user.username == '' ): # not logged in
            return Event.objects.all()
        else:
            if(column):
                if(column=='attending'):
                    return Event.objects.filter(attendees = self.request.user)
                if(column=='zipcode'):
                    try:    return Event.objects.filter(venue__zipcode__contains  = self.request.user.userextension.zipcode)
                    except: return Event.objects.all()
                elif(column=='district'):
                    return Event.objects.filter(venue__district__contains = self.request.user.userextension.district)
                else:
                    return Event.objects.all().order_by(order+column)
            else: return Event.objects.all()

    # def get_context_data(self, *args, **kwargs):
    #     context = super(EventList, self).get_context_data(**kwargs)
    #     context['venue'] = Venue.objects.filter(name = self.request.event.venue)[0]
    #     return context


class EventUpdate(UpdateView):
    model  = Event
    template_name = 'events/event_update.html'
    fields = ['name', 'contact', 'venue', 'date', 'time', 'attendees']

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, self.object.name + " updated")
        return reverse('event_list')
        # return reverse('event_update', kwargs={"pk": self.kwargs['pk']})


class EventDetail(DetailView):
# class EventDetail(UpdateView): 
    model  = Event
    fields = '__all__'
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context   = super(EventDetail, self).get_context_data(**kwargs)
        attendees = context["event"].attendees.all()
        context['attending'] = self.request.user in attendees
        return context

    def post(self, request, **kwargs):
        event = Event.objects.get(id=kwargs['pk'])
        if self.request.user in event.attendees.all():
            event.attendees.remove(self.request.user)
        else:
            event.attendees.add(self.request.user)
        messages.success(self.request, "Attendees updated")
        return HttpResponseRedirect(reverse('event_detail', args=[str(self.kwargs['pk'])]))
        # return render(request, 'events/event_list.html', {'event_list':event_list})
        # return reverse('event_detail', kwargs={"pk": self.kwargs['pk']})


class VenueList(ListView):
    model = Venue
    template_name = 'events/venue_list.html'
    ordering = ['name']

    def get_queryset(self):
        ''' flip sort order '''
        if self.request.session.get('sort_order', '-'):
            self.request.session['sort_order'] = ''
        else:
            self.request.session['sort_order'] = '-'
        order = self.request.session['sort_order']

        ''' column to sort - sent from template '''
        column = self.request.GET.get("column")
        if(column):
            if(column=='zipcode'):
                return Venue.objects.filter(zipcode  = self.request.user.userextension.zipcode)
            elif(column=='district'):
                return Venue.objects.filter(district = self.request.user.userextension.district)
            else:
                return Venue.objects.all().order_by(order+column)
        else: return Venue.objects.all()

    def post(self, request):
        for deleted in request.POST.getlist('delete'):
            Venue.objects.filter(id=deleted).delete()
        venue_list = Venue.objects.all().order_by('name')
        return render(request, self.template_name, {'venue_list':venue_list})

    # class Meta:
    #     ordering = ['name']

    # def get_ordering(self):
    #     ordering = self.request.GET.get('ordering', '-date_created')
    #     # validate ordering here
    #     return ordering


class VenueUpdate(UpdateView):
    model  = Venue
    fields = ['name', 'contact', 'location', 'zipcode']
    template_name = 'events/venue_update.html'

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, self.object.name + " updated")
        return reverse('venue_update', kwargs={"pk": self.kwargs['pk']})


class VenueCreate(CreateView):
    model  = Venue
    fields = ['name', 'location', 'zipcode']
    template_name = 'events/venue_create.html'

    def form_valid(self, form):
         form.instance.contact = self.request.user
         return super(VenueCreate, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, self.object.name + " created")
        return reverse('venue_list')
        # return reverse('venue_update', kwargs={"pk": self.object.pk})


class EventCreate(CreateView):
    model  = Event
    fields = ['name', 'contact', 'venue', 'date', 'time', 'attendees']
    template_name = 'events/event_create.html'

    def form_valid(self, form):
         form.instance.contact = self.request.user
         return super(EventCreate, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, self.object.name + " created")
        return reverse('event_list')
