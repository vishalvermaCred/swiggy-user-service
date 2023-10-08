from typing import Optional
from pydantic import BaseModel, Extra
from pydantic.class_validators import validator
from pydantic.fields import Field

from app.constants import email_regex, phone_regex, Roles, Address


class UserBaseModel(BaseModel):
    class Config:
        use_enum_values = True  # Uses Enum Values
        extra = Extra.ignore  # Ignores Extra Values
        str_strip_whitespace = True  # Removes Whitespaces


class CreateUser(UserBaseModel):
    fullname: str = Field(min_length=1)
    email: str = Field(..., regex=email_regex)
    phone_number: str = Field(..., regex=phone_regex)
    password_hash: str = Field(...)
    address: dict = Field(...)
    vehicle_type: str = Field(None)
    vehicle_registration: str = Field(None)
    role: Roles = Field(...)
    availability: bool = False
    gst_number: Optional[str] = None

    @validator("vehicle_type", "vehicle_registration", "role")
    def validate_data_basis_on_roles(cls, value, values, field):
        if field.name == "role":
            if value == Roles.DELIVERY_PERSONNEL.value and not (
                values.get("vehicle_type") or values.get("vehicle_registration")
            ):
                raise ValueError(
                    f"Vehicle type and Vehicle registeration number are must to register for a Delivery Agent"
                )
        return value

    @validator("address")
    def validate_address(cls, value):
        for key in Address:
            if not value.get(key.value):
                raise ValueError(f"{key.value} for complete address is not provided")
        return value


class GetUsers(BaseModel):
    user_id: Optional[str] = None

    # @root_validator(pre=False)
    # def validate_user(cls, value):
    #     if not value:
    #         raise ValueError(f"user_id is not provided")
    #     return value
