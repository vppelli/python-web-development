from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Recipe

# Create your views here.
def home(request):
   return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
   model = Recipe
   template_name = 'recipes/recipes_list.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
   model = Recipe
   template_name = 'recipes/recipes_detail.html'