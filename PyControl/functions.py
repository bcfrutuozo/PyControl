import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string
import random
import re
import pycountry
import hashlib


def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")


def send_password_reset_email(email, temporary_password):
    # Email configuration
    smtp_server = "mail.frutuozo.com.br"
    smtp_port = 587
    smtp_username = "admin@frutuozo.com.br"
    smtp_password = "hVKpFTVpPC"

    # Email content
    sender_email = "admin@frutuozo.com.br"
    recipient_email = email
    subject = "Password Reset"
    message = f"Your temporary password is: {temporary_password}"

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Disconnect from the server
    server.quit()


def generate_temporary_password(length=8):
    # Generate a random temporary password
    characters = string.ascii_letters + string.digits
    temporary_password = ''.join(random.choice(characters) for letters in range(length))
    return temporary_password


def get_countries():
    country_names_unsorted = [country.name for country in pycountry.countries]
    country_names = sorted(country_names_unsorted)
    return country_names


def validate_country(self, country_name):
    # Check if the entered country is in the list of available countries
    available_countries = self.get_countries()
    return country_name in available_countries


def is_valid_email(email):
    # Regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Use the re.match() function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_chars(input_string):
    # Regular expression pattern to allow only English letters and standard characters
    pattern = re.compile(r'^[a-zA-Z0-9_\-]+$')
    return pattern.match(input_string) is not None


def is_valid_chars_space(input_string):
    # Regular expression pattern to allow only English letters and standard characters
    pattern = re.compile(r'^[a-zA-Z0-9_\- ]+$')
    return pattern.match(input_string) is not None


def encrypt_passphrase(password):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    # Convert the password to bytes and hash it
    hash_object.update(password.encode())
    # Get the hex digest of the hash
    output = hash_object.hexdigest()
    return output
