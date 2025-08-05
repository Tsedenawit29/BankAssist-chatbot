import chromadb

# Ensure storage is persistent
client = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection("bank_users")

def save_user_data(user_data):
    collection.upsert(
        documents=[str(user_data)],
        ids=[user_data["contact"]],
        metadatas=[user_data]
    )

def user_exists(contact):
    try:
        result = collection.get(ids=[contact], include=["metadatas"])
        return bool(result["metadatas"])
    except Exception:
        return False
