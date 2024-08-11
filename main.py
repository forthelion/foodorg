from datetime import datetime
import json
import os
import smtpserver
food_list = []
#food_list_json = os.getenv('FOOD_LIST')
#turn this into text file or someother thing that saves




def save_food_list():
    global food_list
    file_name = "food_list.json"

    # Convert the date to a string in the format YYYY-MM-DD before saving
    food_list_json = json.dumps([{

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
    def __init__(self, name, expiration_date, notes):

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
        return f"  Name: {self.name}, Expires: {self.expiration_date}, Notes: {self.notes}, Status: {status}"





def main():
    def check_food_expired():
        pass
    def add_food_item():
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

                    food_list.append(FoodItem( name, expiration_date, notes))
                    save_food_list()
                    print(f"Item  ({name}) has been added to the list.")

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
            option = input("Enter a command (name(delete),view, exit): ")
            if option == "name":
                name = input("write name of item ")
                food_list = [item for item in food_list if item.name.lower() != name.lower()]
                print(f"{name} has been removed from the list, if it existed.")
                save_food_list()
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

        user_input = input("Enter a command (setup, add, delete, view, notify_expired, exit): ").lower()

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
        elif user_input == 'notify_expired':
            check_food_expired()
        else:
            print(f"Unknown command: {user_input}")

if __name__ == "__main__":
    main()
