from exceptions.APIExceptions import BadRequestException
from schemas import User


def has_valid_initial_id(id: str):
    if id is None:
        return True
    else:
        raise BadRequestException("id has to be set to None")

def has_valid_id(id: str):
    if id is None:
        raise BadRequestException("id cannot be None")

    if not id.isalnum():
        raise BadRequestException("id has to be alphanumeric")

    if id.isspace():
        raise BadRequestException("id cannot be space")

    return True



def has_valid_username(username:str):
    if username is None:
        raise BadRequestException("username cannot be None")

    if username.isspace():
        raise BadRequestException("username cannot be empty")

    if username == "":
        raise BadRequestException("username cannot be empty")

    return True

def has_valid_password(password:str):
    if password is None:
        raise BadRequestException("password cannot be None")

    if password.isspace():
        raise BadRequestException("password cannot be empty")

    if password == "":
        raise BadRequestException("password cannot be empty")
    return True


def validate_user(user:User):
    return has_valid_initial_id(user.id) and has_valid_username(user.username) and has_valid_password(user.password)