from django.urls import URLPattern, path

from .views import (
    chatbot,
    chat_response
)

app_name = 'chatbot'


urlpatterns = [

    path('', chatbot, name="chatbot"),
    path('chatbot-response/', chat_response, name="chatbot-response"),


]