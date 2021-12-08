from django.contrib import admin
from social_django.models import Nonce, Association
from .models import (
    ExchangeInfo,
    Ban,
    Slot,
    Item
)

admin.site.unregister(Nonce)
admin.site.unregister(Association)

admin.site.register((ExchangeInfo, Ban, Slot, Item))

