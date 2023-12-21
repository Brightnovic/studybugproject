from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
def main_view(request):
    context = {}
    return render(request, "livevideo/index.html")

