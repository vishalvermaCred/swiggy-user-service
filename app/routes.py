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
    return {"message": "OK"}


@router.get("/get-user")
async def get_user(request: Request):
    logger.info(f"{LOGGER_KEY}.get_user")
    params = dict(request.query_params)
    headers = dict(request.headers)
    response = await get_user_details(params, headers)
    return await generate_response(**response)


@router.post("/user-signup")
async def create_user(body: CreateUser = Body(...)):
    logger.info(f"{LOGGER_KEY}.create_user")
    validated_data = body.dict()
    phone_number = validated_data.get("phone_number")
    if await user_exists(phone_number):
        return {"status": False, "message": f"User already exists", "code": HTTPStatus.BAD_REQUEST.value}

    response = await onboard_user(validated_data)
    return await generate_response(**response)
