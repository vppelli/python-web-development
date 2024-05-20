import pickle

all_ingredients = []

# Functions ------------------------------------------------------
def display_recipe(recipe):
    print("\n" + "------------------------------------------------------------------------\n" + 
          "Recipe's Ingredients\n" + 
          "------------------------------------------------------------------------")
    print("\n" + "Recipe: ", recipe["name"])
    print("Cooking time: ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

def search_ingredient(data):
    all_ingredients = data["Ingredient list"]
    print("\n" + "------------------------------------------------------------------------\n" + 
          "All Ingredients Available\n" + 
          "------------------------------------------------------------------------")
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}.) {ingredient}")
    try:
        while True:
            answer = int(input("Pick a number from the list of Ingredients: "))
            if 1 <= answer <= len(all_ingredients):
                searched = all_ingredients[answer-1]
                break
            print("Please enter a number between 1 and " + len(all_ingredients))

        recipe_ingredients = [recipe for recipe in data["Recipe list"] if searched in recipe["ingredients"]]

        for recipe in recipe_ingredients:
            display_recipe(recipe)
    
    except ValueError:
        print("Please enter a number.")
    except IndexError:
        print("No such ingredient number.")
        
# Main Code ------------------------------------------------------
print("------------------------------------------------------------------------\n" + 
      "------------------------- SEARCH EVERY RECIPE! -------------------------\n" + 
      "------------------------------------------------------------------------")
filename = input("\n" + "Load a saved file or Create a new file: ") + ".bin"

try:
    with open(filename, "rb") as file:
        data= pickle.load(file)
except FileNotFoundError:
    print("\n" + "File not found, please input a saved file")
except:
    print("\n" + "An Error occured")
else:
    file.close()
finally:
    print("File loaded: " + filename)
    search_ingredient(data)

# End Code ------------------------------------------------------