from  django.urls import path
from .views import *

urlpatterns = [

    path('campaign_contacts_create', CampaignContactsCreate, name='campaign_contacts_create'),
    path('campaign_contacts_delete', CampaignContactsDelete, name='campaign_contacts_delete'),
    path('campaign_contacts_list',   CampaignContactsList,   name='campaign_contacts_list'),
    path('campaign_contacts',        CampaignContacts,       name='campaign_contacts'),
    path('campaign_define',          CampaignDefine,         name='campaign_define'),
    path('campaign_create',          CampaignCreate,         name='campaign_create'),

    # path('event_create',          EventCreate.as_view(), name='event_create'),
    # path('event_update/<int:pk>', EventUpdate.as_view(), name='event_update'),
    # path('event_detail/<int:pk>', EventDetail.as_view(), name='event_detail'),
    # path('venue_list',            VenueList.as_view(),   name='venue_list'),
    # path('venue_create',          VenueCreate.as_view(), name='venue_create'),
    # path('venue_update/<int:pk>', VenueUpdate.as_view(), name='venue_update'),

]
