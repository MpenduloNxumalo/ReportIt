import schemas
from exceptions.APIExceptions import UserNotFoundException, InternalServerErrorException
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: schemas.User):
        return self.repository.create_user(user)

    def retrieve_users(self):
        try:
            return self.repository.retrieve_users()
        except InternalServerErrorException as e:
            raise e

    def retrieve_user(self, user_id):
        try:
            return self.repository.retrieve_user(user_id)
        except UserNotFoundException as e:
            raise e

    def authenticate_user(self, user):
        try:
            return self.repository.authenticate_user(user)
        except UserNotFoundException as e:
            raise e

    def update_user(self, updated_user_id, update: schemas.User):
        try:
            return self.repository.update_user(updated_user_id, update)
        except UserNotFoundException as e:
            raise e
        except InternalServerErrorException as e:
            raise e

    def delete_user(self, deleted_user_id: str):
        try:
            return self.repository.delete_user(deleted_user_id)
        except UserNotFoundException as e:
            raise e
        except InternalServerErrorException as e:
            raise e