from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def read_root():
    raise HTTPException(status_code=404, detail="Endpoint not found")
