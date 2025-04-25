from .database import UserManagementDatabase
from .models import User

user_management_database = UserManagementDatabase()

def login_service(username, password):    
    user = user_management_database.get_user(username)

    if user == None:
        return "User not found"
    
    if user['password'] != password:
        return "Incorrect password"
       
    return user

def get_user_list_service():
    return user_management_database.get_user_list()

def create_user_service(user: User):
    if user.username == "":
        return "Username can't be empty."
    if user.password == "":
        return "Password can't be empty."
    if len(user.permissions) == 0:
        return "At least 1 permission should be assigned."
    
    return user_management_database.create_user(user.username, user.password, user.permissions)

def delete_user_service(username: str):
    if username == "":
        return "Username can't be empty."
    
    return user_management_database.delete_user(username)
    