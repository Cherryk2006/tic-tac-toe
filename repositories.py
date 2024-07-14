from models import *


class UserRepository:

    def find_all(self) -> list:
        return [user for user in User.select()]

    def find_all_order_by_score(self) -> list:
        return [user for user in User.select().order_by(User.score.desc())]

    def find_by_id(self, user_id: int):
        try:
            return User.get(id=user_id)
        except:
            return None

    def create(self, user: User) -> User:
        return User.create(
            id=user.id,
            first_name=user.first_name,
            wins=0,
            loses=0,
            draws=0,
            score=0,
            opponent=None,
            money=0,
            game_mode=0,
            x_skin=user.x_skin,
            o_skin=user.o_skin
        )

    def save(self, user: User):
        return user.save()


class XSkinRepository:

    def find_all_by_users_not_contains(self, user: User) -> list:
        return [x for x in (XSkin.select().where(XSkin.id.not_in([x.id for x in user.x_skins])))]

    def find_by_id(self, x_skin_id: int) -> XSkin:
        return XSkin.get(id=x_skin_id)


class OSkinRepository:

    def find_all_by_users_not_contains(self, user: User) -> list:
        return [o for o in (OSkin.select().where(OSkin.id.not_in([o.id for o in user.o_skins])))]

    def find_by_id(self, o_skin_id: int) -> OSkin:
        return OSkin.get(id=o_skin_id)
