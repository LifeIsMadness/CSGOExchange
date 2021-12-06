from django.contrib.auth.views import auth_logout
from django.shortcuts import render, redirect

from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'exchanger/index.html')


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('auth:index')
