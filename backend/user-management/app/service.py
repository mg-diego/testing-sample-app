from .database import UserManagementDatabase

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