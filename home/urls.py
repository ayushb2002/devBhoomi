from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('state/<slug:state>', views.getStateMap, name="state"),
    path('state/map/<slug:state>', views.sendMap, name="stateMap"),
]
