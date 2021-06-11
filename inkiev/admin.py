from django.contrib import admin
from .models import Event, PrivateEvent, Place

# Register your models here.

admin.site.register(Event)
admin.site.register(PrivateEvent)
admin.site.register(Place)
