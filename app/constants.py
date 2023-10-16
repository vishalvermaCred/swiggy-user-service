"""
    create constants here to be used later
"""

from enum import Enum

PSQL_USER_DB = "user_db"

# regex of phone and email to validate the received phone number and email
phone_regex = r"^(0\d{10}|[1-9]\d{9,11})$"
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


# Enum for Response Keys
class ResponseKeys:
    DATA = "data"
    SUCCESS = "success"
    MESSAGE = "message"
    ERROR = "error"


# Enum containing all the data of tables used
class Tables(Enum):
    USERS = {"name": "users", "columns": ["user_id", "name", "password_hash", "email", "phone_number", "role"]}
    ADDRESSES = {"name": "addresses", "columns": ["user_id", "line", "city", "state", "pincode"]}
    RESTAURANTS = {
        "name": "restaurants",
        "columns": [
            "user_id",
            "gst_number",
        ],
    }
    DELIVERY_PERSONNELS = {
        "name": "delivery_personnels",
        "columns": [
            "user_id",
            "vehicle_type",
            "vehicle_registration",
            "availability",
        ],
    }


# Enum for Roles
class Roles(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    RESTATURANT = "restaurant"
    DELIVERY_PERSONNEL = "delivery_personnel"


# Enum for addresses
class Address(Enum):
    LINE = "line"
    CITY = "city"
    STATE = "state"
    PINCODE = "pincode"
