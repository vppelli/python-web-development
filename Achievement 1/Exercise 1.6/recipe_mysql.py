import mysql.connector

conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="password")

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute("CREATE TABLE IF NOT EXISTS recipes(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), ingredients VARCHAR(255), cooking_time INT, difficulty VARCHAR(20))")

# Functions -------------------------------------------------------------/

# Adds New Recipe -------------------------------------------------------------/
def adding_recipe(conn, cursor):
    n = int(input("\nHow many recipes would you like to create: "))
    f = n
    for i in range(n):
        recipe= new_recipe()
        print("\nRecipe Created!")
        sql = "INSERT INTO recipes(name, ingredients, cooking_time, difficulty) VALUES(%s, %s, %s, %s)"
        val = (recipe["name"], recipe["ingredients"], recipe["cooking_time"], recipe["difficulty"])

        cursor.execute(sql, val)
        conn.commit()
        print("Recipe Added to database!")
        if f >= 2:
            f -= 1
            continue
        print("\nAdded all recipes!")

# Calculate Difficulty -------------------------------------------------------------/
def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"
    
# Called from Add New Recipe -------------------------------------------------------------/
def new_recipe():
    name= input("\nName of recipe: ")
    cooking_time= int(input("Cooking time (min): "))
    ingredients= input("Ingredients | add ', ' for multiple: ").split(", ")
    ingrejoined = ", ".join(ingredients)
    difficulty = calculate_difficulty(cooking_time, ingredients)
    recipe= {"name": name, "cooking_time": cooking_time, "ingredients": ingrejoined, "difficulty": difficulty}
    return recipe

# Search Ingredients in Recipes -------------------------------------------------------------/
def searching_recipe(conn, cursor):
    ingredients_list = set()

    cursor.execute("SELECT ingredients FROM recipes")
    result = cursor.fetchall()

    for recipe in result:
        ingredients = recipe[0]
        ingredients_list.update(ingredients.split(", "))
    
    print("\nAll ingredients available\n")
    for id, ingredient in enumerate(sorted(ingredients_list), start=1):
        print(f"{id}, {ingredient}")
    
    ingredient_number = int(input("\nIngredient Number: ")) - 1
    chosen_ingredient = sorted(ingredients_list)[ingredient_number]

    sql = "SELECT * FROM recipes WHERE ingredients LIKE %s"
    val = f"%{chosen_ingredient}%"
    cursor.execute(sql, (val,))
    result = cursor.fetchall()

    print(f"\nMatching recipes with {chosen_ingredient}")
    for searched in result:
        print(f"\nName: {searched[1]}\nIngredients: {searched[2]}\nCooking Time: {searched[3]}\nDifficulty: {searched[4]}\n-----------------------------")

# Update Name -------------------------------------------------------------/
def update_name(id):
    rename = (input("\nNew recipe name: "))
    sql = "UPDATE recipes SET name = %s WHERE id = %s"
    cursor.execute(sql, (rename, id,))
    cursor.fetchall()
    print(f"\nName changed to {rename}")
    print("-----------------------------")
    return

# Update Cooking time -------------------------------------------------------------/
def update_cooking_time(id):
    newtime = int(input("\nNew cooking time: "))
    sql = "UPDATE recipes SET cooking_time = %s WHERE id = %s"
    cursor.execute(sql, (newtime, id,))
    cursor.fetchall()
    print(f"\nCooking time changed to {newtime} min's")
    print("-----------------------------")
    return

# Update Ingredients -------------------------------------------------------------/   
def update_ingredients(id):
    ingredients= input("Update Ingredients | add ', ' for multiple: ").split(", ")
    ingrejoined = ", ".join(ingredients)
    sql = "UPDATE recipes SET ingredients = %s WHERE id = %s"
    cursor.execute(sql, (ingrejoined, id,))
    cursor.fetchall()
    print(f"\nIngredients updated {ingredients}")
    print("-----------------------------")
    return

# Update Choice Selection -------------------------------------------------------------/
def edit_row(conn, cursor, recipe_number):
    selected_edit = ""
    while(selected_edit != "4"):
        selected_edit = input("\nRow to edit, Type the number: ")
        print("-----------------------------")

        if selected_edit == "1":
            update_name(recipe_number)
            return
        elif selected_edit == "2":
            update_cooking_time(recipe_number)
            return
        elif selected_edit == "3":
            update_ingredients(recipe_number)
            return
        elif selected_edit == "4":
            modify_recipe(conn, cursor)
            return
        else:
            print("Select a Number shown")
    print("Completed")

# Update All Recipes -------------------------------------------------------------/
def modify_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM recipes")
    result = cursor.fetchall()

    print("\nAll recipes available\n")
    for ids, recipes in result:
        recipe = recipes
        id = ids
        print(id, recipe)

    
    recipe_number = int(input("\nRecipe to edit, Type the number: "))
    print("-----------------------------")
    sql = "SELECT * FROM recipes WHERE id = %s"
    cursor.execute(sql, (recipe_number,))
    result = cursor.fetchall()
    for name in result:
        print(f"\nWhat would you like to edit from {name[1]}\n1. Name\n2. Cooking time\n3. Ingredients\n- Difficulty is automaticlly adjusted to change's.\n4. Go back to Recipe select.")

    # Choice Function -------------------------------------------------------------/
    edit_row(conn, cursor, recipe_number)

    sql = "SELECT cooking_time, ingredients FROM recipes WHERE id = %s"
    cursor.execute(sql, (recipe_number,))
    result = cursor.fetchall()

    difficulty = ""
    for cooking_time, ingredients in result:
        time = cooking_time
        length = ingredients.split(",")
        new_difficulty = calculate_difficulty(time, length)
        difficulty = new_difficulty
    
    sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
    cursor.execute(sql, (difficulty, recipe_number,))
    result = cursor.fetchall()

    for modified in result:
        print(f"\nUpdated Recipe\nName: {modified[1]}\nIngredients: {modified[2]}\nCooking Time: {modified[3]}\nDifficulty: {modified[4]}\n-----------------------------")
    
    conn.commit()
# Delete Recipes -------------------------------------------------------------/
def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM recipes")
    result = cursor.fetchall()

    print("\nAll recipes available\n")
    for ids, recipes in result:
        recipe = recipes
        id = ids
        print(id, recipe)

    
    recipe_number = int(input("\nRecipe to delete, Type the number: "))
    print("-----------------------------")
    sql = "SELECT * FROM recipes WHERE id = %s"
    cursor.execute(sql, (recipe_number,))
    result = cursor.fetchall()
    for name in result:
        print(f"\nAre you sure you want to delete {name[1]}\n1. Yes\n2. No")
    choice = input("Your Choice: ")
    if choice == "1":
        sql = "DELETE FROM recipes WHERE id = %s"
        cursor.execute(sql, (recipe_number,))
        print("\nRecipe Deleted!")
    else:
        print("\nAction Canceled returning to Menu!")
    conn.commit()
    print("-----------------------------")

# Main Code -------------------------------------------------------------/
def main_menu(conn, cursor):
    choice = ""
    while(choice != "quit"):
        print("\nWhat would you like to do? Pick a choice!\n\n1. Add a recipe.\n2. Search a recipe.\n3. Edit a recipe.\n4. Remove a recipe.\n Type 'quit' to exit the program.")
        choice = input("\nYour choice: ")
        print("-----------------------------")

        if choice == "1":
            adding_recipe(conn, cursor)
        elif choice == "2":
            searching_recipe(conn, cursor)
        elif choice == "3":
            modify_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "quit":
            conn.commit()
            conn.close()
            print("\nGoodbye!")
            break
        else:
            print("\nSelect a value between 1-4 or 'quit'")
main_menu(conn, cursor)