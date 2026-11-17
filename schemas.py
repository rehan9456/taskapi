from pydantic import BaseModel , Field, EmailStr , ConfigDict


class UserCreate(BaseModel):
    username:str = Field(min_length=3,max_lengh=50)
    email:EmailStr
    password:str=Field(min_length=8,max_lengh=128)

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    is_active:bool

#cleate taske request

class TaskCreate(BaseModel):
    title : str = Field(min_length=3 , max_length=150)
    description :str | None=Field(default=None,max_length=500)
    completed: bool = False

#update task request

# class TaskUpdate(BaseModel):
#     title:str | None = Field(default=None,min_length=3,max_length=150)
#     description : str | None =Field(default=None,max_length=500)
#     completed : bool |  None=None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


#task Response

class TaskResponse(BaseModel):
    id:int
    title :str
    description :str
    completed : bool
    user_id:int

    model_config =ConfigDict(from_attributes=True)
    



