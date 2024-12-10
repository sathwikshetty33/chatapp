from allauth.urls import urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns =[
    path('',chat_view,name='chat'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)