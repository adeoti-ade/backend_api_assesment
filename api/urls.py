from . import views
from django.urls import path


urlpatterns = [
    path("inbound/sms", views.InboundView.as_view()),
    path("outbound/sms", views.OutboundView.as_view()),
    path("token", views.TokenView.as_view())

]
