from  django.urls import path
from .views import VenueList, VenueUpdate, VenueCreate, EventList, EventUpdate, EventDetail, EventCreate

# app_name = "events"
urlpatterns = [

    path('event_list',            EventList.as_view(),   name='event_list'),
    path('event_create',          EventCreate.as_view(), name='event_create'),
    path('event_update/<int:pk>', EventUpdate.as_view(), name='event_update'),
    path('event_detail/<int:pk>', EventDetail.as_view(), name='event_detail'),
    path('venue_list',            VenueList.as_view(),   name='venue_list'),
    path('venue_create',          VenueCreate.as_view(), name='venue_create'),
    path('venue_update/<int:pk>', VenueUpdate.as_view(), name='venue_update'),

]
