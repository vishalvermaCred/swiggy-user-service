from http import HTTPStatus
from fastapi.params import Body
from fastapi import APIRouter, Request
from fastapi.logger import logger

from app.models import CreateUser
from app.service import get_user_details, onboard_user, user_exists
from app.utils import generate_response

router = APIRouter()

LOGGER_KEY = "app.router"


@router.get("/public/healthz")
async def health_check():
    """
    health api of user service to check if user service is working fine or not.
    """
    return {"message": "OK"}


@router.get("/get-user")
async def get_user(request: Request):
    """
    Api to get user details based on user_id
    """
    logger.info(f"{LOGGER_KEY}.get_user")
    params = dict(request.query_params)

    # headers are required to get the role
    headers = dict(request.headers)
    response = await get_user_details(params, headers)
    return await generate_response(**response)


@router.post("/user-signup")
async def create_user(body: CreateUser = Body(...)):
    """
    API to create user on role basis, user can be admin or customer or restuarant or delivery perrsonnel
    """
    logger.info(f"{LOGGER_KEY}.create_user")
    validated_data = body.dict()

    # user uniqueness is based on phone number
    phone_number = validated_data.get("phone_number")
    if await user_exists(phone_number):
        return {"status": False, "message": f"User already exists", "code": HTTPStatus.BAD_REQUEST.value}

    response = await onboard_user(validated_data)
    return await generate_response(**response)
