from django.urls import path
from .views import f_page, private_event_page, public_event_page, public_events, private_events, places, place_page, \
    user_login, logout, user_register, public_events_old, private_events_old, create_private_event, \
    create_public_event, create_place, unverified_places, unverified_public_events, remove_post,\
    deleted_places, deleted_public_events, deleted_private_events, comment_remove

urlpatterns = [
    path('', f_page),
    path('Event/<int:e_pk>/', public_event_page, name='priv'),
    path('Event/', public_events),
    path('Event-old/', public_events_old, name='event-old'),
    path('PrivateEvent/<int:e_pk>/', private_event_page),
    path('PrivateEvent/', private_events),
    path('PrivateEvent-old/', private_events_old),
    path('Place/<int:p_pk>', place_page),
    path('Place/', places),
    path('auth/login/', user_login),
    path("auth/logout/", logout),
    path("auth/register/", user_register),
    path("create-private-event/", create_private_event),
    path("create-public-event/", create_public_event),
    path("create-place/", create_place),
    path("unverified-places/<str:act>/<int:p_pk>/", unverified_places),
    path("unverified-places/", unverified_places),
    path("unverified-public-events/<str:act>/<int:e_pk>/", unverified_public_events),
    path("unverified-public-events/", unverified_public_events),
    path("remove-post/<str:post_class>/<int:p_pk>/", remove_post),
    path("deleted-places/<str:act>/<int:p_pk>/", deleted_places),
    path("deleted-places/", deleted_places),
    path("deleted-public-events/<str:act>/<int:e_pk>/", deleted_public_events),
    path("deleted-public-events/", deleted_public_events),
    path("deleted-private-events/<str:act>/<int:e_pk>/", deleted_private_events),
    path("deleted-private-events/", deleted_private_events),
    path("comment-remove/<int:c_pk>/", comment_remove),
]
