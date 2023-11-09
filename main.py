import requests
import json
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#csv file
with open('data.json', 'r') as file:
    data = json.load(file)

url = 'Your Post Req Endpoint'

email_sender = 'Your email'
email_password = 'Your password'
email_smtp_server = 'smtp.gmail.com'
#generating 8 digit random password
for entry in data:

    password = ''.join(random.choices(string.digits, k=8))

    entry['password'] = password

    print("Payload:", entry)

    response = requests.post(url, json=entry)

    if response.status_code == 200:
        print("POST request successful!")
        print("Response:", response.json())

        email_receiver = entry['emailAddress']

        message = MIMEMultipart()
        message['From'] = email_sender
        message['To'] = email_receiver
        message['Subject'] = 'Generated Password'

        email_content = f"Hello,\n\nYour generated password is: {password}\n\nBest regards,\nYour Sender"

        message.attach(MIMEText(email_content, 'plain'))

        with smtplib.SMTP(email_smtp_server, 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(message)

        print(f"Email sent with password to {email_receiver}.")
    else:
        print("Failed to send POST request. Status code:", response.status_code)
