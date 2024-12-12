from fastapi import APIRouter,HTTPException
from models.todo import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router=APIRouter()

# Get request method
@router.get("/")
async def get_todos():
    try:
        todos = list_serial(collection_name.find())
        return {"status": "success", "data": todos}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))


@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: str):
    try:
        todo_id = ObjectId(todo_id)

        todo = collection_name.find_one({"_id": todo_id})

        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {"status": "success", "data": list_serial([todo])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST request method
@router.post("/")
async def create_todo(todo: Todo):
    try:
       
        new_todo = {
            "name": todo.name,
            "description": todo.description,
            "is_completed": todo.is_completed,
        }
        result = collection_name.insert_one(new_todo)

        
        return {"status": "success", "message": "Todo created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{todo_id}")
async def update_todo(todo_id: str, todo: Todo):
    try:
        todo_id = ObjectId(todo_id)
       
        updated_todo = collection_name.find_one_and_update(
            {"_id": todo_id},
            {"$set": {
                "name": todo.name,
                "description": todo.description,
                "is_completed": todo.is_completed
            }},
            return_document=True 
        )

        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {"status": "success", "message": "Todo updated successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/{todo_id}")
async def delete_todo(todo_id: str):
    try:
        
        todo_id = ObjectId(todo_id)
        result = collection_name.delete_one({"_id": todo_id})

        if result.deleted_count == 0:
            print(f"Todo not found: {todo_id}")
            raise HTTPException(status_code=404, detail="Todo not found")

        return {"status": "success", "message": "Todo deleted successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))