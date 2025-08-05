def get_next_step(user_input, step, user_data):
    if step == "intent":
        if "open" in user_input.lower() and "account" in user_input.lower():
            return "account_type", "What type of account would you like to open? (Savings, Current, Business)"
        else:
            return "intent", "Hi! How can I help you today?"

    elif step == "account_type":
        user_data["account_type"] = user_input.strip()
        return "name", "Great! What's your full name?"

    elif step == "name":
        user_data["name"] = user_input.strip()
        return "address", "Please enter your residential address."

    elif step == "address":
        user_data["address"] = user_input.strip()
        return "id", "Please provide a valid ID number."

    elif step == "id":
        user_data["id"] = user_input.strip()
        return "contact", "What's your phone number or email?"

    elif step == "contact":
        user_data["contact"] = user_input.strip()
        return "confirm", f"""
        Please confirm your details:
        - Name: {user_data['name']}
        - Account Type: {user_data['account_type']}
        - Address: {user_data['address']}
        - ID: {user_data['id']}
        - Contact: {user_data['contact']}
        \nType 'yes' to submit or 'no' to restart.
        """

    elif step == "confirm":
        if "yes" in user_input.lower():
            return "submitted", "🎉 Your application has been submitted!"
        else:
            return "intent", "Okay, let's start over."

    return step, "I'm not sure what to do next."
