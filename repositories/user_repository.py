import schemas
from exceptions.APIExceptions import UserNotFoundException, InternalServerErrorException
from networks.user_network import UserNetwork


class UserRepository:
    def __init__(self, user_network: UserNetwork):
        self.user_network = user_network
        self.db = user_network.get_db()

    def create_user(self, user: schemas.User):
        try:
            document_ref = self.db.collection("User").document()
            document_ref.set(user.model_dump())

            user.id = document_ref.id
            return user
        except Exception as e:
            raise e

    def retrieve_users(self):
        try:
            user_collection = self.db.collection("User")
            documents = user_collection.stream()
            users = []
            for document in documents:
                document_snapshot = document.to_dict()
                user = schemas.User(id=document.id, username=document_snapshot["username"],
                                    password=document_snapshot["password"])
                users.append(user)
            return users

        except InternalServerErrorException as e:
            raise e

    def retrieve_user(self, user_id: str):
        try:
            document_ref = self.db.collection("User").document(user_id)
            document_snapshot = document_ref.get()
            if document_snapshot.exists:
                user = document_snapshot.to_dict()
                user["id"] = document_ref.id
                return user
            else:
                raise UserNotFoundException
        except UserNotFoundException as e:
            raise e

    def retrieve_user_by_username(self, user: schemas.User):
        try:
            user_collection = self.db.collection("User")
            query = user_collection.where("username", "==", user.username).limit(1)
            documents = query.stream()
            for document in documents:
                document_snapshot = document.to_dict()
                if user.username == document_snapshot["username"] and user.password == document_snapshot["password"]:
                    document_snapshot["id"] = document.id
                    return document_snapshot
            raise UserNotFoundException

        except UserNotFoundException as e:
            raise e

    def authenticate_user(self, user):
        try:
            return self.retrieve_user_by_username(user)
        except UserNotFoundException as e:
            raise e

    def update_user(self, updated_user_id: str, update: schemas.User):
        try:
            user_collection = self.db.collection("User")
            document = user_collection.document(updated_user_id)
            if document.get().exists:
                document.update(update.model_dump())
            else:
                raise UserNotFoundException
            return self.retrieve_user(updated_user_id)
        except UserNotFoundException as e:
            raise e
        except InternalServerErrorException as e:
            raise e

    def delete_user(self, id: str):
        try:
            user_collection = self.db.collection("User")
            document = user_collection.document(id)
            if document.get().exists:
                return document.delete()
            else:
                raise UserNotFoundException
        except UserNotFoundException as e:
            raise e
        except InternalServerErrorException as e:
            raise e
