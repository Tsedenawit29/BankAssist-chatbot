def get_next_step(user_input, step, user_data):
    if step == "intent":
        if "open" in user_input.lower() and "account" in user_input.lower():
            return "account_type", "Great! I'd be happy to help you open a new account. 🎉\n\nWhat type of account would you like to open?\n\n• **Savings Account** - Earn interest on your money\n• **Current Account** - For daily transactions and payments\n• **Business Account** - For business operations\n\nPlease type your choice:"
        else:
            return "intent", "Hi! 👋 I'm here to help you with banking services. You can ask me to:\n\n• Open a new account\n• Get information about our services\n• Learn about our products\n\nWhat would you like to do today?"

    elif step == "account_type":
        account_type = user_input.strip().lower()
        if "savings" in account_type:
            user_data["account_type"] = "Savings Account"
            return "name", "Excellent choice! 💰 A savings account is perfect for building your wealth.\n\nPlease provide your full name (as it appears on your ID):"
        elif "current" in account_type:
            user_data["account_type"] = "Current Account"
            return "name", "Great choice! 💳 A current account is ideal for your daily banking needs.\n\nPlease provide your full name (as it appears on your ID):"
        elif "business" in account_type:
            user_data["account_type"] = "Business Account"
            return "name", "Perfect! 🏢 A business account will help you manage your business finances effectively.\n\nPlease provide your full name (as it appears on your ID):"
        else:
            return "account_type", "I didn't quite catch that. Please choose from:\n\n• **Savings Account**\n• **Current Account**\n• **Business Account**\n\nWhich type of account would you like?"

    elif step == "name":
        user_data["name"] = user_input.strip()
        return "address", f"Thank you, {user_data['name']}! 📍\n\nNow, please provide your complete residential address (street, city, postal code):"

    elif step == "address":
        user_data["address"] = user_input.strip()
        return "id", "Perfect! 🆔\n\nPlease provide a valid government-issued ID number (passport, driver's license, or national ID):"

    elif step == "id":
        user_data["id"] = user_input.strip()
        return "contact", "Excellent! 📞\n\nPlease provide your phone number or email address for account notifications:"

    elif step == "contact":
        user_data["contact"] = user_input.strip()
        return "confirm", f"""
        📋 **Application Summary**
        
        Please review your details:
        
        👤 **Name:** {user_data['name']}
        🏦 **Account Type:** {user_data['account_type']}
        📍 **Address:** {user_data['address']}
        🆔 **ID Number:** {user_data['id']}
        📞 **Contact:** {user_data['contact']}
        
        ✅ **Type 'yes' to submit your application**
        ❌ **Type 'no' to start over**
        
        Is everything correct?
        """

    elif step == "confirm":
        if "yes" in user_input.lower():
            return "submitted", f"""
        🎉 **Bank Account Creation Successfully Submitted!**
        
        Thank you, {user_data['name']}! Your {user_data['account_type']} creation request has been successfully submitted to our system.
        
        📞 **We will contact you at {user_data['contact']}** within 2-3 business days to complete the account setup process.
        📧 Please check your email or phone for updates and further instructions.
        
        **What happens next:**
        • Our team will review your application
        • You'll receive a confirmation message at {user_data['contact']}
        • We'll guide you through document verification
        • Your new {user_data['account_type']} will be activated once complete
        
        Thank you for choosing our bank! Is there anything else I can help you with today?
        """
        else:
            return "intent", "No problem! Let's start fresh. 🔄\n\nWhat would you like to do? You can ask me to open a new account or help you with other banking services."

    return step, "I'm not sure what to do next. Could you please try again or ask me to help you open an account?"
