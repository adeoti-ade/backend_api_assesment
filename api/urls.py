from . import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path("inbound/sms", views.InboundView.as_view(), name="inbound"),
    path("outbound/sms", views.OutboundView.as_view(), name="outbound"),
    path("token", views.TokenView.as_view())

]
