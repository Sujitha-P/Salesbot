import json
from datetime import datetime
from config import CRM_DATA_PATH, ALLOWED_PRODUCTS

# Load CRM data from JSON file
def load_crm_data():
    try:
        with open(CRM_DATA_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}  # Return an empty CRM if the file doesn't exist

# Save CRM data to JSON file
def save_crm_data(crm_data):
    with open(CRM_DATA_PATH, "w") as file:
        json.dump(crm_data, file, indent=4)

# Add user interaction to CRM history
def add_user_interaction(email, user_input, action):
    crm_data = load_crm_data()
    for user in crm_data["users"]:
        if user["email"] == email:
            # Extract the product name from the user input
            product = extract_product_name(user_input)
            if product:  # Only save if a product is found
                user["history"].append({
                    "product": product,  # Save only the product name
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                })
            break
    save_crm_data(crm_data)

# Add feedback to CRM
def add_feedback(email, user_input, feedback):
    crm_data = load_crm_data()
    for user in crm_data["users"]:
        if user["email"] == email:
            user["feedback_history"] = user.get("feedback_history", [])
            user["feedback_history"].append({
                "input": user_input,
                "feedback": feedback,
                "timestamp": datetime.now().isoformat()
            })
            break
    save_crm_data(crm_data)

# Check if user exists
def check_existing_user(email):
    crm_data = load_crm_data()
    print(f"Checking CRM data for email: {email}")  # Debugging
    print(f"CRM data: {crm_data}")  # Debugging
    for user in crm_data["users"]:
        if user["email"] == email:
            print("User exists!")  # Debugging
            return True  # User exists
    print("New user detected!")  # Debugging
    return False  # New user

# Get last product searched by user
def get_last_product(email):
    crm_data = load_crm_data()
    for user in crm_data["users"]:
        if user["email"] == email:
            if user.get("history") and len(user["history"]) > 0:
                return user["history"][-1]["product"]  # Return the last product searched
    return None  # No history found

# Extract product name from user input
def extract_product_name(user_input):
    # Convert the input to lowercase for case-insensitive matching
    user_input = user_input.lower()

    # Extract the first matching product keyword
    for product in ALLOWED_PRODUCTS:
        if product in user_input:
            return product

    # If no product is found, return None
    return None

# Whitelist of allowed product keywords
ALLOWED_PRODUCTS = [
    "smart watches", "headphones", "laptops", "smartphones",
    "watches", "earphones", "tablets", "cameras", "printers"
]