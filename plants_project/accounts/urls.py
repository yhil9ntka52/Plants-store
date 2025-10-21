from django.urls import path
from .views import RegisterView, PrivateInfoView, AdminOnlyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('private/', PrivateInfoView.as_view(), name='private-info'),
    path('admin/', AdminOnlyView.as_view(), name='admin-only'),
]
