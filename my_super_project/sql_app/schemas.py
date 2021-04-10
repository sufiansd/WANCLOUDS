'''
pydantic schemas
We are defining our classes and inheriting depending requirements
'''

from typing import List, Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date: str
    

# inherited from ItemBase
class ItemCreate(ItemBase):
    pass

# inherited from ItemBase
class Item(ItemBase):
    id: int
    isLost: int = 1
    isFound: int = 0
    owner_id: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    username: str


# inherited from UserBase
class UserCreate(UserBase):
    password: str

# inherited from UserBase
class User(UserBase):
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
