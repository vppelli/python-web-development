# Functions ------------------------------------------------------
def take_recipe():
    print("")
    name= input("Name of recipe: ")
    time= int(input("Cooking time in min's: "))
    ingredients= input("Ingredients: ").split(", ")
    recipe= {"name": name, "cooking_time": time, "ingredients": ingredients}
    return recipe

def printAllIngredients():
    ingredients_list.sort()
    print("")
    print("All Ingredients Avalible")
    print("------------------------")
    for ingredient in ingredients_list:
        print(ingredient)

def printAllRecipes():
    print("")
    print("All Recipes Created")
    print("------------------------")
    for recipe in recipes_list:
        print("")
        print("Recipe: ", recipe["name"])
        print("Cooking time: ", recipe["cooking_time"])
        print("Ingredients: ")
        for ingredient in recipe["ingredients"]:
            print(ingredient)
        print("Difficulty: ", recipe["difficulty"])

# Main Code ------------------------------------------------------
recipes_list = []
ingredients_list = []

n = int(input("How many recipes would you like to include: "))

for i in range(n):
    recipe= take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    print("Recipe added!")
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"]= "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"]= "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"]= "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"]= "Hard"

# Calls to print ------------------------------------------------------
printAllIngredients()

printAllRecipes()