class Recipe(object):
    # -----------------------           Global Variable           -----------------------
    all_ingredients = set()
    # -----------------------           Initial Area           -----------------------
    def __init__(self, name, cooking_time):
        self.name = name 
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None

    # -----------------------           All About Difficulty Area           -----------------------
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
    
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
        
    # -----------------------           All About Ingredients Area           -----------------------   
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)

    def get_ingredients(self):
        return self.ingredients
    
    def add_ingredients(self, *ingredients):
        for i in ingredients:
            if ingredients not in self.ingredients:
                self.ingredients.append(i)
                self.update_all_ingredients()
            else:
                return f"-> {ingredients}, Already in recipe."
    
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False
        
    # -----------------------           All Remaining Get & Set           -----------------------
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self.name

    def get_cooking_time(self):
        return self.cooking_time
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        return self.cooking_time
    
    def get_all_ingredients(self):
        return Recipe.all_ingredients
    
    def __str__(self):
        self.calculate_difficulty()
        return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}\n"
# -----------------------           End of Class Recipe           -----------------------
    
def recipe_search(list, ingredients):
    print(f"\nRecipes that contain '{ingredients}':\n------------------------")
    for recipes in list:
        if recipes.search_ingredient(ingredients):
            print(f"Recipe Name: {recipes.name}\nDifficulty: {recipes.difficulty}\n")
        
# -----------------------           Main Code Area          -----------------------
            
# Created Recipes ----
print(" \nRecipe Created\n------------------------")
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients("Sugar", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut" "Butter", "Sugar", "Ice Cubes")
print(banana_smoothie)

# Recipe List ----
recipes_list = [tea, coffee, cake, banana_smoothie]

# Recipe for loop ----
print("\nList of All Recipes\n------------------------")
for recipe in recipes_list:
    print(recipe)

# Ingredient for loop ----
for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)