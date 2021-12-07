from django.shortcuts import render, redirect
from django.views import View


class NewTradeView(View):
    def get(self, request):
        return render(request, 'exchanger/trade.html')