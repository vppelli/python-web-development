from django.urls import path
from .views import home

# Create url below
app_name = 'sales'

urlpatterns = [
   path('', home),
]