from django.urls import path
from .views import home

# Create Url below
app_name = 'recipes'

urlpatterns = [
   path('', home),
]