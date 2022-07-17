from django.shortcuts import render
from .models import Chatbot
from chatbot.chatbot import *

from django.http import JsonResponse

# Create your views here.


def chatbot(request):
    request.session['user_name'] = ""
    request.session["user_step"] = 0
    request.session["inputs"] = []
    request.session['asked_for_name'] = 0

   # for key, value in request.session.items():
    #    print('{} => {}'.format(key, value))
    return render(request, 'chatbot/main.html', {'qa':''})


def chat_response(request):
    print(request.GET['input'])

    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    get_response = respond_to_user(request.GET['input'], request)
    return JsonResponse ({'text': get_response})
    