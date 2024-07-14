from telebot import types
from constants import *
from models import User


def base_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🏆Menu🏆")
    btn2 = types.KeyboardButton("🆔Show my id🆔")
    markup.add(btn1, btn2)
    return markup


def menu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="👉Play", callback_data="select_friend_to_play"))
    markup.add(types.InlineKeyboardButton(text="🏅Rating", callback_data="rating"))
    markup.add(types.InlineKeyboardButton(text="🏆My statistic", callback_data="statistic"))

    markup.row(
        types.InlineKeyboardButton(text="❌My skins on X", callback_data="x_skins"),
        types.InlineKeyboardButton(text="⭕My skins on 0", callback_data="o_skins")
    )

    markup.add(types.InlineKeyboardButton(text="🛒Shop", callback_data="shop"))
    markup.add(types.InlineKeyboardButton(text="⚙️Settings", callback_data="setting"))
    return markup


def settings_markup(user: User, message_id) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(text=f"{'✳3×3✳' if user.game_mode == 0 else '3×3'}",
                                   callback_data=f"{'blocked' if user.game_mode == 0 else f'setGameMode 0 {message_id}'}"),
        types.InlineKeyboardButton(text=f"{'✳5×5✳' if user.game_mode == 1 else '5×5'}",
                                   callback_data=f"{'blocked' if user.game_mode == 1 else f'setGameMode 1 {message_id}'}"),
        types.InlineKeyboardButton(text=f"{'✳8×8✳' if user.game_mode == 2 else '8×8'}",
                                   callback_data=f"{'blocked' if user.game_mode == 2 else f'setGameMode 2 {message_id}'}")
    )
    return markup


def choose_x_skins_markup(user: User, message_id: int) -> types.InlineKeyboardMarkup:
    counter = 0
    lst = []
    markup = types.InlineKeyboardMarkup()
    for x in [x for x in user.x_skins]:
        if counter == 3:
            markup.row(*lst)
            lst = []
            counter = 0
        lst.append(types.InlineKeyboardButton(text=f"{f'✳{x.skin}✳' if x.id == user.x_skin.id else f'{x.skin}'}"
                                              ,
                                              callback_data=f"{f'blocked' if x.id == user.x_skin.id else f'set_x_skin {x.id} {message_id}'}"
                                              ))
        counter += 1

    if len(lst) > 0:
        markup.row(*lst)

    return markup


def choose_o_skins_markup(user: User, message_id: int) -> types.InlineKeyboardMarkup:
    counter = 0
    lst = []
    markup = types.InlineKeyboardMarkup()
    for o in [o for o in user.o_skins]:
        if counter == 3:
            markup.row(*lst)
            lst = []
            counter = 0
        lst.append(types.InlineKeyboardButton(text=f"{f'✳{o.skin}✳' if o.id == user.o_skin.id else f'{o.skin}'}"
                                              ,
                                              callback_data=f"{f'blocked' if o.id == user.o_skin.id else f'set_o_skin {o.id} {message_id}'}"
                                              ))
        counter += 1

    if len(lst) > 0:
        markup.row(*lst)

    return markup


def shop_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(text=X_SKIN_BUTTON_TEXT, callback_data="x_shop"),
        types.InlineKeyboardButton(text=O_SKIN_BUTTON_TEXT, callback_data="o_shop")
    )

    return markup


def x_skin_shop_markup(x_skins: list, message_id: int) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for x_skin in x_skins:
        markup.add(
            types.InlineKeyboardButton(text=f"{x_skin.skin} - {x_skin.price}",
                                       callback_data=f"buy_x {x_skin.id} {message_id}")
        )

    return markup


def o_skin_shop_markup(o_skins: list, message_id: int) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for o_skin in o_skins:
        markup.add(
            types.InlineKeyboardButton(text=f"{o_skin.skin} - {o_skin.price}",
                                       callback_data=f"buy_o {o_skin.id} {message_id}")
        )

    return markup


def get_score_board(user_list: list, current_user: User) -> str:
    place = 1
    result = ""
    for user in user_list:
        if place == 1:
            result += "🥇: "
        elif place == 2:
            result += "🥈: "
        elif result == 3:
            result += "🥉: "
        else:
            for digit in str(place):
                result += f"{DIGITS_ICON[int(digit)]}: "

        if user.id == current_user.id:
            result += "👉"

        result += f'{user.first_name} - {user.score}🎖\n'
        place += 1

    return result
