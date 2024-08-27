from django.urls import path
from .views import DomainCheckView, IPCheckView, HashCheckView

urlpatterns = [
    path('api/check-domain/', DomainCheckView.as_view(), name='check-domain'),
    path('api/check-ip/', IPCheckView.as_view(), name='check-ip'),
    path('api/check-hash/', HashCheckView.as_view(), name='check-hash'),
]
