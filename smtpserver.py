import os
import subprocess
from email.message import EmailMessage
import ssl
import smtplib
import main

email = os.getenv('EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')

def has_email_password():
    return bool(email and email_password and smtp_server)

def is_email_setUp():
    if not has_email_password():
        print("You need to setup email, program can not send updates if food spoil  ")
        setUp()
def setUp():

    global email, email_password, smtp_server
    email_services = {
        "gmail": "smtp.gmail.com",
        "yahoo": "smtp.mail.yahoo.com",
        "outlook": "smtp-mail.outlook.com"
    }
    print("Please input your email service. Currently supporting:")
    for service in email_services.keys():
        print(f"- {service}")

    # ask users for email
    while True:
        email_service = input("Email service: ").strip().lower()
        if email_service not in email_services:
            print("Unsupported email service. Please choose from the list above.")
            continue
        email = input("Please enter your email: ")
        email_password = input("Please enter your email: ")
        smtp_server = email_services[email_service]
        # ask users for pasword saves

        os.environ['EMAIL'] = email
        os.environ['EMAIL_PASSWORD'] = email_password
        os.environ['SMTP_SERVER'] = smtp_server

        success = send_test_email()
        if success:
            received = input("Did you receive the test email? (yes/no): ")
            if received.lower() == 'yes':
                return True
            else:
                print("Resending test email...")
                send_test_email()
        else:
            print("Failed to send the test email.")




def send_test_email():
    try:
        subject = 'test'
        body = 'test message'
        em = EmailMessage()
        em['From'] = email
        em['To'] = email_password
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        # make it so you can swap  email
        with smtplib.SMTP_SSL( smtp_server, 465, context=context) as smtp:
            smtp.login( email, email_password)
            smtp.sendmail(email, email, em.as_string())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_message( food, data_of_food):

    subject = 'alert'+ food +'spoiled'
    body = data_of_food
    em = EmailMessage()
    em['From'] = email
    em['To'] = email_password
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    # make it so you can swap  email
    with smtplib.SMTP_SSL( smtp_server, 465, context=context) as smtp:
        smtp.login( email, email_password)
        smtp.sendmail(email, email, em.as_string())
