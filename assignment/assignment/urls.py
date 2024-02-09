from api.views.BalanceView import BalanceView
from api.views.EventView import EventView
from api.views.ResetView import ResetView
from django.urls import path

urlpatterns = [
    path('balance', BalanceView.as_view()),
    path('event', EventView.as_view()),
    path('reset', ResetView.as_view())
]
