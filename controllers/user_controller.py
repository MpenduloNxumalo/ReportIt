from fastapi import status, APIRouter, HTTPException

import schemas
from exceptions.APIExceptions import BadRequestException, InternalServerErrorException, UserNotFoundException
from networks.user_network import UserNetwork
from repositories.user_repository import UserRepository
from services.user_service import UserService
from utils.user_utils import validate_user, has_valid_id, has_valid_username, has_valid_password

router = APIRouter()
user_network = UserNetwork()
user_repository = UserRepository(user_network)
user_service = UserService(user_repository)


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User):
    try:
        if validate_user(user):
            return user_service.create_user(user)
        else:
            raise InternalServerErrorException("An invalid user failed to trigger bad request exception.")
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InternalServerErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/authenticate_user", status_code=status.HTTP_200_OK)
def authenticate_user(user: schemas.User):
    try:
        if validate_user(user):
            return user_service.authenticate_user(user)
        else:
            raise InternalServerErrorException("An invalid user failed to trigger bad request exception.")
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InternalServerErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/retrieve_users")
def retrieve_all_users():
    try:
        return user_service.retrieve_users()
    except InternalServerErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/retrieve_user/{id}")
def retrieve_user(id: str):
    try:
        if has_valid_id(id):
            return user_service.retrieve_user(id)
        else:
            raise InternalServerErrorException("An invalid user id failed to trigger bad request exception.")
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update_user/{updated_user_id}", status_code=status.HTTP_201_CREATED)
def update_user(updated_user_id: str, update: schemas.User):
    try:
        if has_valid_id(updated_user_id) and has_valid_username(update.username) and has_valid_password(
                update.password):
            return user_service.update_user(updated_user_id, update)
        else:
            raise InternalServerErrorException("An invalid user failed to trigger bad request exception.")
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except InternalServerErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete_user/{deleted_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(deleted_user_id: str):
    try:
        if has_valid_id(deleted_user_id):
            return user_service.delete_user(deleted_user_id)
        else:
            raise InternalServerErrorException("An invalid user failed to trigger bad request exception.")
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except InternalServerErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))