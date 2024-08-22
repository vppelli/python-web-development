from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField(help_text='Spaced ingredients with a ", "')
    cooking_time = models.IntegerField(help_text='time in minutes')
    difficulty = models.CharField(max_length=120,default='Easy')
    pic = models.ImageField(upload_to='recipes', default='no-picture.png')
    about = models.TextField(default='No info')

    def __str__(self):
        return f"Name: {self.name}\nIngredients: {self.ingredients}\nCooking Time: {self.cooking_time}\n Difficulty: {self.difficulty}"
    
    def get_absolute_url(self):
        return reverse('recipes:recipes_detail', kwargs={'pk': self.pk})