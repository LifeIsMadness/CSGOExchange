from django.db import models
from authentication.models import SteamUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# TODO: auto create this model for the new user
class ExchangeInfo(models.Model):
    user = models.OneToOneField(
        to=SteamUser,
        related_name='exchange_info',
        on_delete=models.CASCADE
    )
    count = models.IntegerField(default=0)


# if its permanent ban - no end time
class Ban(models.Model):
    user = models.ForeignKey(
        to=SteamUser,
        on_delete=models.CASCADE,
        related_name='bans'
    )
    reason = models.TextField(default='Rules violation')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True)


# check if added_at - now() >= 30 min
# then call save() to refresh
class Slot(models.Model):
    user = models.ForeignKey(
        to=SteamUser,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    added_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25)

    class Meta:
        ordering = ['-added_at']

    def get_bump(self):
        now = timezone.now()
        return (now - self.added_at).seconds // 60


# now only weapons
class Item(models.Model):
    class Types(models.Choices):
        KEY = 'Key'
        KNIFE = 'Knife'
        PISTOL = 'Pistol'
        RIFLE = 'Rifle'
        SHOTGUN = 'Shotgun'
        SMG = 'SMG'
        SNIPER_RIFLE = 'Sniper Rifle'
        MACHINEGUN = 'Machinegun'
        TOOL = 'Tool'
        PASS = 'Pass'
        CONTAINER = 'Container'
        STICKER = 'Sticker'
        TAG = 'Tag'
        KIT = 'Kit'
        GIFT = 'Gift'
        COLLECTIBLE = 'Collectible'
        GRAFFITI = 'Graffiti'
        GLOVES = 'Gloves'
        MUSIC_KIT = 'Music Kit'
        AGENT = 'Agent'
        PATCH = 'Patch'

    item_id = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=100, choices=Types.choices, null=True)
    name = models.CharField(max_length=255, default='')
    market_name = models.CharField(max_length=255, default='')
    market_hash_name = models.CharField(max_length=255, default='')
    lowest_price = models.CharField(max_length=20, default='')
    image_link = models.CharField(
        max_length=1000,
        default=''
    )
    exterior = models.CharField(max_length=20, null=True)
    inventory = models.ForeignKey(
        to='Inventory',
        related_name='items',
        on_delete=models.CASCADE,
        null=True
    )
    slots = models.ManyToManyField(to='Slot')

    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.name.__str__()


# Auto-created after the user is created
class Inventory(models.Model):
    raw_data = models.JSONField(null=True)
    trade_link = models.URLField(max_length=500, null=True)
    user = models.OneToOneField(
        to=SteamUser,
        related_name='inventory',
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=SteamUser)
def create_inventory(sender, **kwargs):
    if kwargs.get('created'):
        Inventory.objects.create(user=kwargs.get('instance'))
