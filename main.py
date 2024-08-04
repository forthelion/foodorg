from datetime import datetime
from email.mime.text import MIMEText
import smtpserver

food_list = []
unique_number_counter = 1



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
            self.send_message(self.name, data_of_food)
            return True
        else:
            return False

    def __str__(self):
        status = "Expired" if self.is_expired() else "Fresh"
        return f"ID: {self.unique_number}, Name: {self.name}, Expires: {self.expiration_date}, Notes: {self.notes}, Status: {status}"



def main():
    def add_food_item():
        global unique_number_counter

        while True:
            smtpserver.is_email_setUp()
            name = input("Enter the food name: ").strip()
            if any(item.name.lower() == name.lower() for item in food_list):
                print(f"An item with the name '{name}' already exists. Please enter a unique name.")
                continue
            notes = input("Enter any notes: ")
            while True:
                expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")
                try:
                    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
                    food_list.append(FoodItem(unique_number_counter, name, expiration_date, notes))
                    print(f"Item {unique_number_counter} ({name}) has been added to the list.")
                    unique_number_counter += 1
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            while True:
                user_input = input("do you want to add another food item enter 'yes' or exit enter 'exit'.")
                if user_input == 'exit':
                    print("Exiting the program. Goodbye!")
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
            elif option == "number":
                try:
                    number = int(input("Enter the item number to delete: ").strip())
                    original_length = len(food_list)
                    food_list = [item for item in food_list if item.unique_number != number]
                    if len(food_list) < original_length:
                        print(f"Item number {number} has been removed from the list.")
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

    while True:
        smtpserver.is_email_setUp()
        user_input = input("Enter a command (setup,add, delete, view, exit): ").lower()

        if user_input == 'exit':
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
