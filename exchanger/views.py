from django.shortcuts import render, redirect
from django.views import View
from string import Template
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.utils import timezone
import datetime
from .models import Item

INVENTORY_URL = Template('https://steamcommunity.com/profiles/$steamid/inventory/json/730/2')
PRICE_URL = Template('https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=$name')
ICON_URL = Template('https://steamcommunity-a.akamaihd.net/economy/image/$icon')


class NewTradeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        inventory = user.inventory
        if not inventory.items.all().exists():
            self._update_inventory(inventory, user.steamid)
            inventory.save()

        if (timezone.now() - inventory.updated_at) >= \
                datetime.timedelta(minutes=10):
            self._update_inventory(inventory, user.steamid)
            inventory.save()

        context = {
            'items': inventory.items.all(),
            'refreshed_at': (timezone.now() - inventory.updated_at).seconds // 60

        }
        return render(request, 'exchanger/trade.html', context=context)

    def _update_inventory(self, inventory, steam_id):
        data = requests.get(INVENTORY_URL.substitute(steamid=steam_id))
        if data.status_code == 200:
            self._parse_inventory(data.json(), inventory)

    def _parse_inventory(self, data, inventory):
        def get_item_data(item_data):
            tags = item_data['tags']
            exterior, type_ = None, None
            for v in tags:
                vals = v.values()
                if 'Exterior' in vals:
                    exterior = v['name']
                if 'Type' in vals:
                    type_ = v['name']

            price_data = requests.get(PRICE_URL.substitute(name=item_data['market_hash_name']))
            lowest_price = price_data.json().get('lowest_price', None)
            res = {
                'type': type_,
                'name': item_data['name'],
                'market_name': item_data['market_name'],
                'market_hash_name': item_data['market_hash_name'],
                'image_link': ICON_URL.substitute(icon=item_data['icon_url']),
                'exterior': exterior,
                'lowest_price': lowest_price,
            }
            return res

        ids = list(data['rgInventory'].values())
        items = list(data['rgDescriptions'].values())
        instances = inventory.items.all()
        for item in instances:
            if not item.slots.all().exists() and item.item_id not in map(str, ids):
                continue
            item.delete()

        for i in range(len(ids)):
            for k in range(len(items)):
                if ids[i]['classid'] != items[k]['classid']:
                    continue
                if items[k]['tradable'] == 0:
                    continue
                if instances.filter(item_id=ids[i]['id']).exists():
                    continue

                Item.objects.create(
                    inventory=inventory,
                    item_id=ids[i]['id'],
                    **get_item_data(items[k]),
                )

