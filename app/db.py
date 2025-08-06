import chromadb
import time
import os

# Ensure storage is persistent with timeout settings
try:
    client = chromadb.PersistentClient(
        path="./chroma_storage",
        settings=chromadb.Settings(
            chroma_server_http_port=8000,
            chroma_server_host="localhost",
            anonymized_telemetry=False
        )
    )
    collection = client.get_or_create_collection("bank_users")
except Exception as e:
    print(f"Database initialization error: {e}")
    # Fallback to in-memory client if persistent fails
    client = chromadb.Client()
    collection = client.get_or_create_collection("bank_users")

def save_user_data(user_data):
    """Save user data to the database with retry logic"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            collection.upsert(
                documents=[str(user_data)],
                ids=[user_data["contact"]],
                metadatas=[user_data]
            )
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database save attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                # If all retries failed, try to save to a simple file as backup
                try:
                    import json
                    backup_file = "./backup_users.json"
                    backup_data = []
                    
                    # Load existing backup data
                    if os.path.exists(backup_file):
                        with open(backup_file, 'r') as f:
                            backup_data = json.load(f)
                    
                    # Add new user data
                    backup_data.append(user_data)
                    
                    # Save to backup file
                    with open(backup_file, 'w') as f:
                        json.dump(backup_data, f, indent=2)
                    
                    print(f"Data saved to backup file: {backup_file}")
                    return True
                except Exception as backup_error:
                    raise Exception(f"Database and backup both failed. DB error: {str(e)}, Backup error: {str(backup_error)}")

def user_exists(contact):
    """Check if a user with this contact (phone/email) already exists"""
    try:
        # Check by exact contact match
        result = collection.get(ids=[contact], include=["metadatas"])
        if result["metadatas"]:
            return True
            
        # Also check if contact exists in any metadata (for better duplicate detection)
        all_results = collection.get(include=["metadatas"])
        for metadata in all_results["metadatas"]:
            if metadata and metadata.get("contact") == contact:
                return True
                
        return False
    except Exception:
        return False

def is_duplicate_contact(contact):
    """Check if phone number or email already exists in the database"""
    try:
        # Normalize contact for comparison
        contact = contact.strip().lower()
        
        # Get all users from database
        all_results = collection.get(include=["metadatas"])
        
        for metadata in all_results["metadatas"]:
            if metadata and "contact" in metadata:
                existing_contact = metadata["contact"].strip().lower()
                
                # Check for exact match
                if existing_contact == contact:
                    return True
                    
                # Check if it's a phone number (contains only digits, +, -, spaces, parentheses)
                if contact.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit():
                    # Normalize phone numbers for comparison
                    normalized_contact = contact.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
                    normalized_existing = existing_contact.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
                    if normalized_contact == normalized_existing:
                        return True
                        
        return False
    except Exception as e:
        print(f"Error checking duplicate contact: {e}")
        return False

def get_user_by_contact(contact):
    """Get user data by contact information"""
    try:
        result = collection.get(ids=[contact], include=["metadatas"])
        if result["metadatas"]:
            return result["metadatas"][0]
        return None
    except Exception:
        return None
