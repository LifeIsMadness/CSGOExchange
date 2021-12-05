from django.db import models
from authentication.models import SteamUser


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


# now only weapons
class Item(models.Model):
    class Types(models.Choices):
        KNIFE = 'knife'
        PISTOL = 'pistol'
        RIFLE = 'rifle'
        SHOTGUN = 'shotgun'
        SMG = 'smg'
        SNIPER_RIFLE = 'sniper rifle'

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=Types.choices)
    cost = models.DecimalField(max_digits=21, decimal_places=20)
    image = models.ImageField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name.__str__()


class Weapon(Item):
    pass


# TODO: could be choices
class WeaponSkin(models.Model):
    name = models.CharField(max_length=255)
    quality = models.CharField(max_length=20)
    float = models.FloatField()
    weapon = models.ForeignKey(
        to='Weapon',
        related_name='skins',
        on_delete=models.CASCADE
    )
    slots = models.ManyToManyField(to='Slot')
