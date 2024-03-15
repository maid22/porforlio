import requests  #A COOK BOOK

APIKEY = "549eab7e042544fca2d3981ca49db354"

def main():
    continue_program = True
    while continue_program:
        try:
            query = input("What's your craving? ")
            cuisine =input("Which cuisine are you interested in? ")
            calorie = int(input("What's the maximum calories allowed?"))
        except ValueError as err:
            print(err,"is not a number")
        else:
            print(food_list(query,cuisine,calorie))

        try:
            my_ID = int(input("What's the ID of your dish? "))
            value = how_to_cook(my_ID)
        except ValueError as err:
            print(err,"It is not a correct ID number")
        except IndexError as err:
            print(err,"It is not a correct ID number")
        else:
            print(value)
            ask = input("Would you like to save this recipe? y/n ")
            if ask == "y":
                myname = input("How would you name your file?")
                save_recipe(myname,value)
                continue_program = False
            else:
                print("GoodBye")
                continue_program = False


def food_list(query,cuisine,calorie) -> str:
    if not isinstance(calorie,int):
        raise ValueError("Not an integer")
    food = []
    parameter ={
        "apiKey":APIKEY,
        "query": query,
        "cuisine": cuisine ,
        "maxCalories": calorie
    }
    food_response = requests.get("https://api.spoonacular.com/recipes/complexSearch",params= parameter)
    food_response.raise_for_status()
    my_food = food_response.json()["results"]
    for f in my_food:
        if "nutrition" in f and "nutrients" in f["nutrition"] and len(f["nutrition"]["nutrients"])>0 and "amount" in f["nutrition"]["nutrients"][0]:
            food.append((f"{f["title"]}, ID: {f["id"]}, Calories: {f["nutrition"]["nutrients"][0]["amount"]}"))
        else:
            continue
    my_food = "\n".join(food)
    return my_food


def how_to_cook(number : int) -> str:
    instructions = []
    if not isinstance(number,int):
        raise ValueError("Not an integer")
    response = requests.get(f"https://api.spoonacular.com/recipes/{number}/analyzedInstructions?apiKey={APIKEY}")
    response.raise_for_status()
    data = response.json()
    for s in data[0]["steps"]:#it is a list of dict
        if isinstance(s,dict):
            instructions.append(f"Step {s['number']}: {s['step']}\n")
    formatted_instructions = "\n".join(instructions)
    return formatted_instructions


#it takes a string as an argument and writes it to a file. The filename is determined by user input.
def save_recipe(myname,value):
    with open(f"{myname}.txt","w") as file:
        file.write(f"{value}")

if __name__ == "__main__":
    main()
#refactor your code so that the input can be passed as a function argument instead.That's a good step towards making your function more testable! Now, you can easily control the inputs to your function in your tests
