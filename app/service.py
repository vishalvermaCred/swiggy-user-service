from uuid import uuid4
from http import HTTPStatus
from fastapi.logger import logger

from app.context import app_context
from app.constants import Tables, Roles

LOGGER_KEY = "app.service"


async def user_exists(phone_number):
    logger.info(f"{LOGGER_KEY}.check_if_user_exists")
    select_query = f"select user_id from {Tables.USERS.value['name']} where phone_number = '{phone_number}';"
    user_data = await app_context.db.execute_raw_select_query(select_query)
    if user_data:
        return True
    return False


async def add_user(kwargs):
    """
    this function will add standard user details in users table
    """
    logger.info(f"{LOGGER_KEY}.create_user")
    try:
        # unique user id for user
        user_id = uuid4().hex
        user_insert_response = {"error": None, "user_id": None}
        user_columns = ", ".join(Tables.USERS.value["columns"])

        # preparing insert query
        insert_user_query = f"INSERT INTO {Tables.USERS.value['name']} ({user_columns}) VALUES ('{user_id}', '{kwargs.get('fullname')}', '{kwargs.get('password_hash')}', '{kwargs.get('email')}', '{kwargs.get('phone_number')}', '{kwargs.get('role')}');"

        # executing insertion
        insert_response = await app_context.db.execute_insert_or_update_query(insert_user_query)
        logger.info(f"insert_response: {insert_response}")
        user_insert_response["user_id"] = user_id
        logger.info(f"{LOGGER_KEY}.add_user.user_id: {user_id}")
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.create_user.exceptiopn: {str(e)}")
        user_insert_response["error"] = str(e)
        user_insert_response["code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
    # returns the user id
    return user_insert_response


async def add_address(kwargs):
    """
    creates the entry of user's address in addresses table and returns the response
    """
    logger.info(f"{LOGGER_KEY}.add_addresses")
    try:
        address_details = kwargs.get("address")
        address_table_columns = ", ".join(Tables.ADDRESSES.value["columns"])
        insert_address_query = f"INSERT INTO {Tables.ADDRESSES.value['name']} ({address_table_columns}) VALUES ('{kwargs.get('user_id')}', '{address_details.get('line')}', '{address_details.get('city')}', '{address_details.get('state')}', '{address_details.get('pincode')}');"
        insert_response = await app_context.db.execute_insert_or_update_query(insert_address_query)
        logger.info(f"insert_response: {insert_response}")
        return {"success": True, "message": "Admin User created successfully", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.add_addresses.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}


async def add_restaurant(kwargs):
    """
    pushes resturant details into restaurant table
    """
    logger.info(f"{LOGGER_KEY}.create_restaurant")

    try:
        columns = ", ".join(Tables.RESTAURANTS.value["columns"])
        insert_query = f"INSERT INTO {Tables.RESTAURANTS.value['name']} ({columns}) VALUES ('{kwargs.get('user_id')}', '{kwargs.get('gst_number')}');"
        insert_response = await app_context.db.execute_insert_or_update_query(insert_query)
        logger.info(f"insert_response: {insert_response}")
        return {"success": True, "message": "Admin User created successfully", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.add_restaurant.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}


async def add_delivery_personnel(kwargs):
    """
    pushes delivery personnel's details delivery_personnels table
    """
    logger.info(f"{LOGGER_KEY}.add_delivery_personnel")
    try:
        columns = ", ".join(Tables.DELIVERY_PERSONNELS.value["columns"])
        insert_query = f"INSERT INTO {Tables.DELIVERY_PERSONNELS.value['name']} ({columns}) VALUES ('{kwargs.get('user_id')}', '{kwargs.get('vehicle_type')}', '{kwargs.get('vehicle_registration')}', '{kwargs.get('availability')}');"
        insert_response = await app_context.db.execute_insert_or_update_query(insert_query)
        logger.info(f"insert_response: {insert_response}")
        return {"success": True, "message": "Admin User created successfully", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.add_restaurant.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}


async def onboard_user(kwargs):
    """
    Basis on the role, user is created and entry is created in dedicated tables
    """
    logger.info(f"{LOGGER_KEY}.onboard_user")
    try:
        user_creation_response = await add_user(kwargs)
        if user_creation_response.get("error"):
            return {
                "success": False,
                "message": user_creation_response.get("error"),
                "code": user_creation_response.get("code"),
            }
        user_id = user_creation_response.get("user_id")
        kwargs["user_id"] = user_id

        # Address of users is handled separately
        address_creation_response = await add_address(kwargs)
        if not address_creation_response.get("success"):
            return address_creation_response

        # basis on the role restaurant and delivery personnel gets created.
        role = kwargs.get("role")
        if role == Roles.RESTATURANT.value:
            restaurant_creation_response = await add_restaurant(kwargs)
            if not restaurant_creation_response.get("success"):
                return restaurant_creation_response
        elif role == Roles.DELIVERY_PERSONNEL.value:
            delivery_personnel_creation_response = await add_delivery_personnel(kwargs)
            if not delivery_personnel_creation_response.get("success"):
                return delivery_personnel_creation_response

        return {"success": True, "message": "User created successfully", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.onboard_admin.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}


async def get_user_details(kwargs, headers):
    """
    on the basis of user_id this function gets user data from all the suitable tables and returns the merged data of user
    """
    logger.info(f"{LOGGER_KEY}.get_user_details")
    try:
        # extracting the filters
        user_id = kwargs.get("user_id")
        role = headers.get("role")

        # preparing the queries to extract data from DB
        if role in [Roles.ADMIN.value or Roles.CUSTOMER.value]:
            select_query = f"SELECT u.name, u.email, u.phone_number, a.line, a.city, a.state, a.pincode From {Tables.USERS.value['name']} u inner join {Tables.ADDRESSES.value['name']} a using (user_id) where u.user_id = '{user_id}';"
        if role == Roles.RESTATURANT.value:
            select_query = f"SELECT u.name, u.email, u.phone_number, a.line, a.city, a.state, a.pincode, r.gst_number From {Tables.USERS.value['name']} u inner join {Tables.ADDRESSES.value['name']} a using (user_id) INNER JOIN {Tables.RESTAURANTS.value['name']} r using (user_id) where u.user_id = '{user_id}';"
        if role == Roles.DELIVERY_PERSONNEL.value:
            select_query = f"SELECT u.name, u.email, u.phone_number, a.line, a.city, a.state, a.pincode, d.vehicle_type, d.vehicle_registration, d.availability From {Tables.USERS.value['name']} u inner join {Tables.ADDRESSES.value['name']} a using (user_id) INNER JOIN {Tables.DELIVERY_PERSONNELS.value['name']} d using (user_id) where u.user_id = '{user_id}';"

        # Executing query
        user_data = await app_context.db.execute_raw_select_query(select_query)
        logger.info(f"{LOGGER_KEY}.get_user_details.user_data: {user_data}")

        # handling response
        if not user_data:
            return {"success": False, "message": "user does not exists", "code": HTTPStatus.BAD_REQUEST.value}
        return {
            "success": True,
            "message": "user data fetched successfully",
            "code": HTTPStatus.OK.value,
            "data": user_data,
        }
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.get_user_details.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}
