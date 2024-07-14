from peewee import *

db = SqliteDatabase('db/tic_toe_bot_db.db')


class BaseModel(Model):
    class Meta:
        database = db


class Skin(BaseModel):
    id = AutoField(primary_key=True)
    skin = CharField(null=False)
    price = IntegerField()


class XSkin(Skin):
    class Meta:
        db_table = 'x_skin'


class OSkin(Skin):
    class Meta:
        db_table = 'o_skin'


class User(BaseModel):
    class Meta:
        db_table = 'usr'

    id = PrimaryKeyField()
    first_name = CharField()
    wins = IntegerField()
    loses = IntegerField()
    draws = IntegerField()
    score = IntegerField()
    opponent = ForeignKeyField('self', to_field="id")
    money = IntegerField()
    game_mode = IntegerField()
    x_skin = ForeignKeyField(XSkin, to_field="id")
    o_skin = ForeignKeyField(OSkin, to_field="id")
    x_skins = ManyToManyField(XSkin, backref="users")
    o_skins = ManyToManyField(OSkin, backref="users")
