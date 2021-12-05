from django.contrib import admin
from social_django.models import UserSocialAuth, Nonce, Association
from .models import (
    ExchangeInfo,
    Ban,
    Slot,
    Weapon,
    WeaponSkin
)

admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)

admin.site.register((ExchangeInfo, Ban, Slot, Weapon, WeaponSkin))

