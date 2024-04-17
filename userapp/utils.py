import uuid

def generate_order_id():
    # Generate a UUID (Universally Unique Identifier) and return its hex representation
    return uuid.uuid4().hex[:10]  