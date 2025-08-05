import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\+?[0-9]{7,15}$", phone)

def format_name(name):
    return name.strip().title()
