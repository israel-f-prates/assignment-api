from api.views import BalanceView
from api.views import EventView
from api.views import ResetView
from api.views import CoffeeView
from django.urls import path

urlpatterns = [
    path('balance', BalanceView.as_view()),
    path('event', EventView.as_view()),
    path('reset', ResetView.as_view()),
    path('coffee', CoffeeView.as_view())
]
