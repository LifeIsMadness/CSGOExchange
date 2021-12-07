from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from exchanger.views import NewTradeView

app_name = 'exchanger'

urlpatterns = [
    url(r'^trade/new/$', NewTradeView.as_view(), name='trade'),
]
