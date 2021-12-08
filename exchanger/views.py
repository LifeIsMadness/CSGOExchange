from django.shortcuts import render, redirect, reverse
from django.views import View
from string import Template
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.utils import timezone
import datetime
from .models import Item, Slot
from django.views.generic import ListView
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models import Q

INVENTORY_URL = Template('https://steamcommunity.com/profiles/$steamid/inventory/json/730/2')
PRICE_URL = Template('https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=$name')
ICON_URL = Template('https://steamcommunity-a.akamaihd.net/economy/image/$icon')


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'exchanger/index.html'
    paginate_by = 15
    context_object_name = 'slots'

    def get_queryset(self):
        search = ''.join(self.request.GET.get('search', ''))
        queryset = Slot.objects.filter(status='active').prefetch_related('item_set')
        return queryset

    def get_context_data(self, **kwargs):
        print(self.object_list)
        context = super().get_context_data(**kwargs)
        trade_link = self.request.user.inventory.trade_link
        context['trade_link'] = trade_link
        print(context)

        return context


class TradelinkRequiredView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tradelink_required.html')


class TradelinkForm(forms.Form):
    trade_link = forms.URLField(max_length=500, required=True)


class SetupTradelinkView(LoginRequiredMixin, View):
    def post(self, request):
        form = TradelinkForm(request.POST)
        if form.is_valid():
            trade_link = form.cleaned_data['trade_link']
            inv = request.user.inventory
            inv.trade_link = trade_link
            inv.save()
            return redirect(reverse('exchanger:index'))
        return render(request, 'tradelink_required.html')


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
        print(ids)
        items = list(data['rgDescriptions'].values())
        instances = inventory.items.all()
        for item in instances:
            if item.item_id not in map(lambda x: x['id'], ids):
                for slot in item.slots.all():
                    slot.status = 'closed'
                    slot.save()
                item.inventory = None
                item.save()

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


class AddSlot(LoginRequiredMixin, View):
    def post(self, request):
        data = dict(request.POST)

        data.pop('csrfmiddlewaretoken')
        ids = data.keys()
        slot = Slot.objects.create(
            user=request.user,
            status='active'
        )
        for id in ids:
            item = Item.objects.get(item_id__exact=id)
            slot.item_set.add(item)
        slot.save()
        return redirect(reverse('exchanger:index'))


class MyTrades(LoginRequiredMixin, ListView):
    template_name = 'exchanger/my_trades.html'
    paginate_by = 15
    context_object_name = 'slots'

    # queryset = Slot.objects.all().prefetch_related('item_set')

    def get_queryset(self):
        return Slot.objects.filter(
            user=self.request.user,
            status='active'
        ).prefetch_related('item_set')

    def get_queryset(self):
        search = self.request.GET.get('search', [''])[0]
        queryset = Slot.objects.filter(user=self.request.user).filter(status='active').prefetch_related('item_set')
        return  queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trade_link = self.request.user.inventory.trade_link
        context['trade_link'] = trade_link
        return context


class MyHistory(LoginRequiredMixin, ListView):
    template_name = 'exchanger/my_history.html'
    paginate_by = 15
    context_object_name = 'slots'

    # queryset = Slot.objects.all().prefetch_related('item_set')


    def get_queryset(self):
        search = self.request.GET.get('search', [''])[0]
        queryset = Slot.objects.filter(user=self.request.user).filter(status='closed').prefetch_related('item_set')
        return  queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trade_link = self.request.user.inventory.trade_link
        context['trade_link'] = trade_link
        return context


class BumpSlot(LoginRequiredMixin, View):
    def get(self, request, id):
        get_object_or_404(Slot, user=request.user, pk=id, status='active').save()
        return redirect(reverse('exchanger:my_trades'))


class CloseSlot(LoginRequiredMixin, View):
    def get(self, request, id):
        slot = get_object_or_404(Slot, user=request.user, pk=id, status='active')
        slot.status = 'closed'
        slot.save()
        return redirect(reverse('exchanger:my_trades'))
