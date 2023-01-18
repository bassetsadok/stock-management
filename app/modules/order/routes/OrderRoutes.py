from fastapi import   status,HTTPException,Depends,APIRouter

router=APIRouter(
    prefix="/order",
    tags=["Order"]
)
