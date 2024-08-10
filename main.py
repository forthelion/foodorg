from datetime import datetime
import json
import os
import smtpserver
food_list = []
#food_list_json = os.getenv('FOOD_LIST')
#turn this into text file or someother thing that saves
unique_number_counter = 1



def save_food_list():
    global food_list
    file_name = "food_list.json"

    # Convert the date to a string in the format YYYY-MM-DD before saving
    food_list_json = json.dumps([{
        "unique_number": item.unique_number,
        "name": item.name,
        "expiration_date": item.expiration_date.strftime("%Y-%m-%d"),  # Convert date to string
        "notes": item.notes
    } for item in food_list], indent=4)  # Pretty-print with indentation

    # Write the JSON data to the file
    with open(file_name, "w") as file:
        file.write(food_list_json)
    # test
    # print(f"{file_name} has been updated.")

# Function to save the food list into environment variables
def load_food_list():
    global food_list
    file_name = "food_list.json"

    # Check if the file exists
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            food_list_json = file.read()

        if food_list_json:
            food_list_data = json.loads(food_list_json)
            food_list = [
                FoodItem(
                    unique_number=item["unique_number"],
                    name=item["name"],
                    expiration_date=datetime.strptime(item["expiration_date"], "%Y-%m-%d").date(),
                    # Convert string back to date
                    notes=item["notes"]
                ) for item in food_list_data
            ]
            # testing
            #print(f"{file_name} loaded successfully.")

    else:
        # If file doesn't exist, create it with default content (e.g., an empty list)
        food_list_data = []
        with open(file_name, "w") as file:
            json.dump(food_list_data, file, indent=4)
        food_list = []
        # for testing
        #print(f"{file_name} created with default content.")




class FoodItem:
    def __init__(self, unique_number, name, expiration_date, notes):
        self.unique_number = unique_number
        self.name = name
        self.expiration_date = expiration_date
        self.notes = notes

    def is_expired(self):
        # update word
        current_date = datetime.now().date()
        if current_date > self.expiration_date:
            data_of_food = str(self)
            smtpserver.send_message(self.name, data_of_food)
            return True
        else:
            return False

    def __str__(self):
        status = "Expired" if self.is_expired() else "Fresh"
        return f"ID: {self.unique_number}, Name: {self.name}, Expires: {self.expiration_date}, Notes: {self.notes}, Status: {status}"



def main():

    def add_food_item():
        global unique_number_counter
        unique_number_counter = len(food_list) + 1
        smtpserver.is_email_setUp()
        while True:

            name = input("Enter the food name: ").strip()
            if any(item.name.lower() == name.lower() for item in food_list):
                print(f"An item with the name '{name}' already exists. Please enter a unique name.")
                continue
            notes = input("Enter any notes: ")
            while True:
                expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")
                try:
                    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()

                    # prevents food that exspire  today or past it will not  be added to the list
                    if expiration_date <= datetime.now().date():
                        print("The expiration date cannot be today or in the past. Please enter a valid future date.")
                        continue

                    food_list.append(FoodItem(unique_number_counter, name, expiration_date, notes))
                    save_food_list()
                    print(f"Item {unique_number_counter} ({name}) has been added to the list.")
                    unique_number_counter += 1
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            while True:
                user_input = input("do you want to add another food item enter 'yes' or exit enter 'exit'.")
                if user_input == 'exit':
                    print("leaving method to add food to list ")
                    return
                elif user_input == 'yes':
                    break
                else:
                    print("please type the command again")

    def delete_food_item():
        global food_list
        smtpserver.is_email_setUp()
        while True:
            view_food_list()
            option = input("Enter a command (name(to delete by name),enter(to delete by number),view, exit): ")
            if option == "name":
                name = input("write name of item ")
                food_list = [item for item in food_list if item.name.lower() != name.lower()]
                print(f"{name} has been removed from the list, if it existed.")
                save_food_list()
            elif option == "number":
                try:
                    number = int(input("Enter the item number to delete: ").strip())
                    original_length = len(food_list)
                    food_list = [item for item in food_list if item.unique_number != number]
                    if len(food_list) < original_length:
                        print(f"Item number {number} has been removed from the list.")
                        save_food_list()
                    else:
                        print(f"No item found with the number {number}.")
                except ValueError:
                    print("Please enter a valid number.")
            elif option == "exit":
                break
            else:
                print("can you try again ")

    def view_food_list():
        smtpserver.is_email_setUp()
        if food_list:
            for item in food_list:
                print(item)
        else:
            print("The food list is empty.")

    load_food_list()
    while True:
        smtpserver.is_email_setUp()

        user_input = input("Enter a command (setup,add, delete, view, exit): ").lower()

        if user_input == 'exit':
            save_food_list()
            print("Exiting the program. Goodbye!")
            break
        elif user_input == 'setup':
            has_email_password = smtpserver.setUp()
        elif user_input == 'add':
            add_food_item()
        elif user_input == 'delete':
            delete_food_item()
        elif user_input == 'view':
            view_food_list()
        else:
            print(f"Unknown command: {user_input}")

if __name__ == "__main__":
    main()
