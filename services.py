from repositories import *


class UserService:

    def __init__(self, user_repository: UserRepository,
                 x_skin_repository: XSkinRepository,
                 o_skin_repository: OSkinRepository):
        self.user_repository = user_repository
        self.x_skin_repository = x_skin_repository
        self.o_skin_repository = o_skin_repository

    def find_all_order_by_score(self) -> list:
        return self.user_repository.find_all_order_by_score()

    def get_or_create(self, user: User) -> User:
        user_from_db = self.user_repository.find_by_id(user.id)
        if user_from_db is None:
            default_x_skin = self.x_skin_repository.find_by_id(1)
            default_o_skin = self.o_skin_repository.find_by_id(1)
            default_x_skin2 = self.x_skin_repository.find_by_id(2)
            default_o_skin2 = self.o_skin_repository.find_by_id(2)
            user.x_skin = default_x_skin
            user.o_skin = default_o_skin
            user.x_skins = [default_x_skin, default_x_skin2]
            user.o_skins = [default_o_skin, default_o_skin2]
            return self.user_repository.create(user)
        return user_from_db

    def get_x_skin_shop_for_user(self, user: User) -> list:
        return self.x_skin_repository.find_all_by_users_not_contains(user)

    def get_o_skin_shop_for_user(self, user: User) -> list:
        return self.o_skin_repository.find_all_by_users_not_contains(user)

    def save(self, user: User) -> User:
        self.user_repository.save(user)
        return self.user_repository.find_by_id(user.id)

    def set_x_skin_for_user(self, x_skin_id: int, user: User) -> User:
        new_x_skin = self.x_skin_repository.find_by_id(x_skin_id)
        user.x_skin = new_x_skin
        self.user_repository.save(user)
        return self.user_repository.find_by_id(user.id)

    def set_o_skin_for_user(self, o_skin_id: int, user: User) -> User:
        new_o_skin = self.o_skin_repository.find_by_id(o_skin_id)
        user.o_skin = new_o_skin
        self.user_repository.save(user)
        return self.user_repository.find_by_id(user.id)

    def buy_x_skin(self, x_skin_id: int, user: User) -> int:
        x_skin = self.x_skin_repository.find_by_id(x_skin_id)
        if user.money >= x_skin.price:
            user.money -= x_skin.price
            new_x_skins = [x for x in user.x_skins]
            new_x_skins.append(x_skin)
            user.x_skins = new_x_skins
            self.user_repository.save(user)
            return user.money
        return user.money - x_skin.price

    def buy_o_skin(self, o_skin_id: int, user: User) -> int:
        o_skin = self.o_skin_repository.find_by_id(o_skin_id)
        if user.money >= o_skin.price:
            user.money -= o_skin.price
            new_o_skins = [x for x in user.o_skins]
            new_o_skins.append(o_skin)
            user.o_skins = new_o_skins
            self.user_repository.save(user)
            return user.money
        return user.money - o_skin.price
