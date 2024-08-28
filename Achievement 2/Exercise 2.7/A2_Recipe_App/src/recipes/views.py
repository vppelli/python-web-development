from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import RecipesSearchForm
import pandas as pd
from .utils import get_chart, get_recipename_from_id

# Create your views here.
def home(request):
   return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
   model = Recipe

   def get(self,request):
      form = RecipesSearchForm()
      recipes = Recipe.objects.all()
      return render(request, 'recipes/recipes_list.html', {'form': form, 'recipes': recipes})
   
   def post(self, request):
      #create an instance of searcg that was defined in recipes/forms.py
      form = RecipesSearchForm(request.POST)
      recipes_df = None     #initialize dataframe to None
      chart = None        #initialize chart to None

      #check if the button is clicked
      if form.is_valid():
         #read recipe_title and chart_type
         recipe_title = form.cleaned_data.get('recipe_title')
         chart_type = form.cleaned_data.get('chart_type')

         #apply filter to extract data
         qs = Recipe.objects.filter(name__icontains = recipe_title)
         if qs:          #if data found
            #convert the queryset values to pandas dataframe
            recipes_df=pd.DataFrame(qs.values())
            # recipes_df['name'] = recipes_df['name'].apply(get_recipename_from_id)
            #calls get_chart() function
            chart=get_chart(chart_type, recipes_df, labels=recipes_df['name'].values)
            #convert data into html
            recipes_df=recipes_df.to_html()

      #pack up data to be sent to template in the context dictionary
      context={
         'form': form,
         'recipes_df': recipes_df,
         'chart': chart,
      }

      #Load recipes_search.html page using data from form  
      return render(request, 'recipes/recipes_list.html', context)

class RecipeDetailView(LoginRequiredMixin, DetailView):
   model = Recipe
   template_name = 'recipes/recipes_detail.html'