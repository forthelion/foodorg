# FoodAlert

The program is designed for the user to manipulate a database of food items with their expiration date. The user can create, view, or delete food items from the database. The program automatically saves the user's operations. The main purpose is to alert the user, via an email, when the program is asked to check for expired items.

Before running the program, you will need a Gmail account with an enabled alternative app password (follow this guide to do it https://www.youtube.com/watch?v=QGGAZxdPX9A)

Launch the program with "python .\main.py"

The program will show the commands and options it supports.

To avoid entering your email information on every run set up the following Environment variables:
    * EMAIL (put your email), 
    * EMAIL_PASSWORD (recommendation: use alternative app password)
    * SMTP_SERVER, which is just "smtp.gmail.com" as the two other email services dont work for now.

 