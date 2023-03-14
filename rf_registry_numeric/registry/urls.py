from django.urls import path
from registry.api_views import FindPhoneView
from registry.views import form_view

urlpatterns = [
    path("api/find-phone/", FindPhoneView.as_view()),
    path("", form_view),
]
