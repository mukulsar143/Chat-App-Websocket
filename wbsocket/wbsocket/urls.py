
from django.contrib import admin
from django.urls import path, include
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/user/', GetUser.as_view()),
    path('api/user/message/', MessageListCreateAPIView.as_view()),
]
