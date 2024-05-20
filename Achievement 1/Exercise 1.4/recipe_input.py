import pickle

# Functions ------------------------------------------------------
def take_recipe():
    name= input("\n" + "Name of recipe: ")
    time= int(input("\n" + "Cooking time in min's: "))
    ingredients= input("\n" + "Ingredients, seperated by a comma: ").split(", ")
    difficulty= calc_difficulty(time, ingredients)
    recipe= {"name": name, "cooking_time": time, "ingredients": ingredients, "difficulty": difficulty}
    return recipe

def calc_difficulty(time, ingredients):
    if time < 10 and len(ingredients) < 4:
        difficulty= "Easy"
        return difficulty
    elif time < 10 and len(ingredients) >= 4:
        difficulty= "Medium"
        return difficulty
    elif time >= 10 and len(ingredients) < 4:
        difficulty= "Intermediate"
        return difficulty
    elif time >= 10 and len(ingredients) >= 4:
        difficulty= "Hard"
        return difficulty
    
def printAllIngredients():
    ingredients_list.sort()
    print("\n" + "------------------------------------------------------------------------\n" + 
        "All Ingredients Available\n" + 
        "------------------------------------------------------------------------")
    for ingredient in ingredients_list:
        print(ingredient)

def printAllRecipes():
    print("\n" + "------------------------------------------------------------------------\n" + 
          "All Recipe's Available\n" + 
          "------------------------------------------------------------------------")
    for recipe in recipes_list:
        print("")
        print("Recipe: ", recipe["name"])
        print("Difficulty: ", recipe["difficulty"])

# Main Code ------------------------------------------------------
recipes_list = []
ingredients_list = []

print("------------------------------------------------------------------------\n" + 
      "----------------------- SAVE EVERY RECIPE TODAY! -----------------------\n" + 
      "------------------------------------------------------------------------")
filename = input("\n" + "Load a saved file or Create a new file: ") + ".bin"

try:
    file= open(filename, "rb")
    data= pickle.load(file)
except FileNotFoundError:
    print("\n" + "File not found, Creating a new file now!")
    data = {"Recipe list": recipes_list, "Ingredient list": ingredients_list}
except:
    print("\n" + "An Error occured")
    data = {"Recipe list": recipes_list, "Ingredient list": ingredients_list}
else:
    file.close()
finally:
    print("File loaded: " + filename)
    recipes_list = data["Recipe list"]
    ingredients_list = data["Ingredient list"]
    printAllRecipes()
    printAllIngredients()

amount = int(input("\n" + "------------------------------------------------------------------------\n" + 
                   "How many recipes would you like to add: "))

for i in range(amount):
    recipe= take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    print("\n" + "Recipe added!")
    recipes_list.append(recipe)

# End Code ------------------------------------------------------
with open(filename, "wb") as file:
    pickle.dump(data, file)
    print("\n" + "------------------------------------------------------------------------\n" + 
          "Your file has been updated.\nlocation: " + filename + "\n" + 
          "------------------------------------------------------------------------")


