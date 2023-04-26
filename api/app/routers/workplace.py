from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/")
async def get_workplace():
    """ Get the """
    return {"message": "Hello World"}
