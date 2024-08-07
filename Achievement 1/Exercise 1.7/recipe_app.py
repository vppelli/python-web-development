import os
from dotenv import load_dotenv
load_dotenv()
info = os.getenv("EXPO_PUBLIC_SQLKEY")
from sqlalchemy import create_engine
engine = create_engine(info)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "\nRecipe ID: " + str(self.id) + " - " + self.name + ": " + self.difficulty
    
    def __str__(self):
        return f"\nRecipe: {self.name}\nIngredients: {self.ingredients}\nCooking time: {self.cooking_time} min's\nDifficulty: {self.difficulty}"
    
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            return "Intermediate"
        else:
            return "Hard"
    
    def return_ingredients_as_list(self):
        ingredients = self.ingredients.split(", ")
        return ingredients
    
Base.metadata.create_all(engine)
# Reusable Validation Loops
def name_valid():
    while True:
        try:
            name = input("\nName of recipe: ")
            if len(name) > 50:
                print("Name must be less than 50 characters")
            else:
                break
        except ValueError:
            print("Please input a valid name.")
    return name
def cooking_time_valid():
    while True:
        try:
            cooking_time = int(input("Cooking time (min): "))
            break
        except ValueError:
            print("Please input a valid number.")
    return cooking_time
def amount_of_ingredients_valid():
    while True:
        try:
            ia = int(input("\nYour Choice: "))
            break
        except ValueError:
            print("Please input a valid number.")
    return ia

# Menu Functions to call  
def create_recipe():
    # Called from for loop to input recipe information
    def new_recipe():
        ingredient_list = []
        # Uses Validation loop setup above.
        name = name_valid()
        cooking_time = cooking_time_valid()
        print("\nHow many ingredients would you like to create: ")
        ia = amount_of_ingredients_valid()
        
        for amount in range(ia):
            ingredient = input("Ingredient: ")
            if ingredient not in ingredient_list:
                ingredient_list.append(ingredient)
        print("\nAll ingredients added!")
        ingredients = ", ".join(ingredient_list)

        recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)

        recipe_entry.difficulty = recipe_entry.calculate_difficulty()

        session.add(recipe_entry)
        session.commit()
        return recipe_entry.name
    # Asks how many recipes you want then for loops it.
    n = int(input("\nHow many recipes would you like to create: "))
    f = n

    for i in range(n):
        recipe = new_recipe()
        print(f"\nRecipe {recipe} Created!")
        if f >= 2:
            f -= 1
            continue
        print("\nAdded all recipes!")
    return

def view_all_recipes():
    if session.query(Recipe).count() == 0:
        print("Recipe list is empty!")
        return
    
    recipe_list = session.query(Recipe).all()
    for recipe in recipe_list:
        print(recipe)

def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("List is empty!")
        return
    
    all_ingredients = set()
    results = session.query(Recipe).all()
    for ingredients in results:
        ingredient = ingredients.return_ingredients_as_list()
        all_ingredients.update(ingredient)

    print("\nAll ingredients available\n")
    for id, ingredient in enumerate(sorted(all_ingredients), start=1):
        print(f"{id}, {ingredient}")
    
    while True:
            # Checks if selected number is Valid
            try:
                ingredient_number = int(input("\nIngredient Number: ")) - 1
                chosen_ingredient = sorted(all_ingredients)[ingredient_number]
                recipe = session.query(Recipe).filter(Recipe.ingredients.like(f"%{chosen_ingredient}%")).all()
                if not recipe:
                    print("That number is not listed!\nTry again.")
                else:
                    break
            except ValueError:
                print("Please input a valid number.")

    for found in recipe:
        print(found)
    return

def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("Recipe list is empty!")
        return
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("\nAll recipes available\n")
    for ids, names in results:
        name = names
        id = ids
        print(id, name)
    
    while True:
            # Checks if selected number is Valid
            try:
                recipe_number = amount_of_ingredients_valid()
                recipe_to_edit = session.get(Recipe, recipe_number)
                if not recipe_to_edit:
                    print("That number is not listed!\nTry again.")
                else:
                    break
            except ValueError:
                print("Please input a valid number.")

    print("-----------------------------")
    print(f"\nWhat would you like to edit from {recipe_to_edit.name}\n1. Name\n2. Cooking time\n3. Ingredients\n4. Go back to Menu.\nNote. Difficulty is automaticlly adjusted to change's.")

    edit_column = ""
    while True:
        # Uses Validation loop setup above.
        ingredient_list = []

        edit_column = input("\nType a number: ")
        print("-----------------------------")
        if edit_column == "1":
            recipe_to_edit.name = name_valid()
            session.commit()
            break
        elif edit_column == "2":
            recipe_to_edit.cooking_time = cooking_time_valid()
            session.commit()
            break
        elif edit_column == "3":
            print("\nHow many ingredients would you like to create: ")
            ia = amount_of_ingredients_valid()
            for amount in range(ia):
                ingredient = input("Ingredient: ")
                if ingredient not in ingredient_list:
                    ingredient_list.append(ingredient)
            print("\nAll ingredients added!")
            ingredients = ", ".join(ingredient_list)
            recipe_to_edit.ingredients = ingredients
            session.commit()
            break
        elif edit_column == "4":
            break
        else:
            print("Select a Number shown")
            continue
    print("Completed")
    return

def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("List is empty!")
        return
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("\nAll recipes available\n")
    for ids, names in results:
        name = names
        id = ids
        print(id, name)
    
    while True:
            try:
                recipe_to_delete = amount_of_ingredients_valid()
                recipe = session.query(Recipe).filter(Recipe.id == recipe_to_delete).one()
                if not recipe:
                    print("That number is not listed!\nTry again.")
                else:
                    break
            except ValueError:
                print("Please input a valid number.")
    print(f"Are you sure you want to delete {recipe.name}\n1. Yes\n2. No")
    
    # Uses Validation loop setup above.
    confimed_value = amount_of_ingredients_valid()

    if confimed_value == 1:
        print(f"Recipe: {recipe.name} Deleted!")
        session.delete(recipe)
        session.commit()
    else:
        print("Canceled operation, returning to Menu ")
        return
    return

# Main Code 
def main_menu():
    choice = ""
    while(choice != "quit"):
        print("\nWhat would you like to do? Pick a choice!\n\n1. Add a recipe.\n2. View all recipes\n3. Search by ingredient.\n4. Edit a recipe.\n5. Remove a recipe.\n Type 'quit' to exit the program.")
        choice = input("\nYour choice: ")
        print("-----------------------------")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("\nGoodbye!")
            break
        else:
            print("\nSelect a value between 1-4 or 'quit'")

main_menu()
# End Session and Engine
session.close()
engine.dispose()