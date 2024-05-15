from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from instorage.main.models import DateTimeModelMixin, IDModelMixin


class ProfileBase(BaseModel):
    full_name: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    """
    The only field required to create a profile is the users id
    """

    user_id: int


class ProfileUpdate(ProfileBase):
    """
    Allow users to update any or no fields, as long as it's not user_id
    """

    pass


class ProfileInDB(IDModelMixin, DateTimeModelMixin, ProfileBase):
    user_id: int
    username: Optional[str]  # will be inherited from User
    email: Optional[EmailStr]  # will be inherited from User


class ProfilePublic(ProfileInDB):
    pass
