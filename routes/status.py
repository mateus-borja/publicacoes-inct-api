from fastapi import APIRouter

entry_root = APIRouter()
@entry_root.get("/")
def apiRunning():
    return {"status": "OK", 
            "message": "API is running."
            }