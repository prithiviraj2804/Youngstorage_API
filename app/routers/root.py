from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"message": "welcome to the Youngstorage API server", "status": True}