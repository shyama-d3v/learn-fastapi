def serializer(todo)->dict:
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "is_completed": todo["is_completed"]
    }
    
def list_serial(todos)->list:
    return [serializer(todo) for todo in todos]
    