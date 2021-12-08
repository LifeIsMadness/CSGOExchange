from django.conf.urls import url
from django.urls import path
from exchanger.views import (
    NewTradeView,
    IndexView,
    TradelinkRequiredView,
    SetupTradelinkView,
    AddSlot,
    BumpSlot,
    CloseSlot,
    MyTrades,
    MyHistory
)

app_name = 'exchanger'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^trade/new/$', NewTradeView.as_view(), name='trade'),
    url(r'^setup/tradelink/$', SetupTradelinkView.as_view(), name='tradelink'),
    url(r'^trade/add_slot/$', AddSlot.as_view(), name='add_slot'),
    url(r'^trade/my_trades/$', MyTrades.as_view(), name='my_trades'),
    url(r'^trade/my_history/$', MyHistory.as_view(), name='my_history'),
    path('trade/close/<int:id>/', CloseSlot.as_view(), name='close_trade'),
    path('trade/bump/<int:id>/', BumpSlot.as_view(), name='bump_trade'),
    url(r'^tradelink_required/$',
        TradelinkRequiredView.as_view(),
        name='tradelink_required'),
]
