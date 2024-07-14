import telebot
from services import *
from repositories import *
from helper import *
from secret import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
user_service = UserService(UserRepository(), XSkinRepository(), OSkinRepository())


def send_message(text: str, chat_id: int, markup) -> types.Message:
    return bot.send_message(chat_id, text, reply_markup=markup)


def edit_message(text: str, chat_id: int, markup, message_id: int) -> types.Message:
    return bot.edit_message_text(text, chat_id, message_id, reply_markup=markup)


def delete_message(chat_id: int, message_id: int):
    bot.delete_message(chat_id=chat_id, message_id=message_id)


@bot.message_handler(commands=['start'])
def start_handler(message):
    user = user_service.get_or_create(User(
        id=message.from_user.id,
        first_name=message.from_user.first_name
    ))
    send_message(
        f'Hello, {user.first_name}! Welcome to Tic-Toe Bot!',
        message.from_user.id,
        base_markup()
    )


@bot.message_handler(content_types=['text'])
def start_handler(message):
    user = user_service.get_or_create(User(
        id=message.from_user.id,
        first_name=message.from_user.first_name
    ))
    if message.text == "🏆Menu🏆":
        send_message("🏆Menu🏆", user.id, menu_markup())
    elif message.text == "🆔Show my id🆔":
        send_message(f'{user.id}', user.id, base_markup())


@bot.callback_query_handler(func=lambda callback: True)
def query_handler(callback):
    user = user_service.get_or_create(User(
        id=callback.from_user.id,
        first_name=callback.from_user.first_name
    ))

    data = str(callback.data)

    if data == "statistic":
        count_of_games = user.wins + user.draws + user.loses
        win_percentage = 0 if count_of_games == 0 else user.wins / count_of_games * 100
        send_message(
            f'''
▶️ Total games played: {count_of_games}
📊 Win percentage: {win_percentage}
🎖 Rating: {user.score}
                
🏆 Wins: {user.wins}
🤕 Defeats: {user.loses}
⚖️ Draws: {user.draws}
💵 Money: {user.money}
            ''',
            user.id,
            base_markup()
        )
    elif data == "rating":
        users = user_service.find_all_order_by_score()
        send_message(get_score_board(users, user), user.id, base_markup())
    elif data == "setting":
        message = send_message(SETTING_MESSAGE, user.id, None)
        edit_message(SETTING_MESSAGE, user.id, settings_markup(user, message.message_id), message.message_id)
    elif data.startswith("setGameMode"):
        new_mode, message_id = map(int, data.split(" ")[1:])
        user.game_mode = new_mode
        user_from_db = user_service.save(user)
        edit_message(SETTING_MESSAGE, user_from_db.id, settings_markup(user_from_db, message_id), message_id)
    elif data == "x_skins":
        message = send_message(f"{user.first_name}, {CHOSE_SKIN_MESSAGE}", user.id, None)
        edit_message(
            f"{user.first_name}, {CHOSE_SKIN_MESSAGE}",
            user.id,
            choose_x_skins_markup(user, message.message_id),
            message.message_id
        )
    elif data.startswith("set_x_skin"):
        new_x_skin_id, message_id = map(int, data.split(" ")[1:])
        user_from_db = user_service.set_x_skin_for_user(new_x_skin_id, user)
        edit_message(
            f"{user_from_db.first_name}, {CHOSE_SKIN_MESSAGE}",
            user_from_db.id,
            choose_x_skins_markup(user_from_db, message_id),
            message_id
        )
    elif data == "o_skins":
        message = send_message(f"{user.first_name}, {CHOSE_SKIN_MESSAGE}", user.id, None)
        edit_message(
            f"{user.first_name}, {CHOSE_SKIN_MESSAGE}",
            user.id,
            choose_o_skins_markup(user, message.message_id),
            message.message_id
        )
    elif data.startswith("set_o_skin"):
        new_o_skin_id, message_id = map(int, data.split(" ")[1:])
        user_from_db = user_service.set_o_skin_for_user(new_o_skin_id, user)
        edit_message(
            f"{user_from_db.first_name}, {CHOSE_SKIN_MESSAGE}",
            user_from_db.id,
            choose_o_skins_markup(user_from_db, message_id),
            message_id
        )
    elif data == "shop":
        send_message(SHOP_MESSAGE, user.id, shop_markup())
    elif data == "x_shop":
        x_skins_in_shop = user_service.get_x_skin_shop_for_user(user)
        if len(x_skins_in_shop) == 0:
            send_message(X_SKIN_SHOP_EMPTY_MSG, user.id, base_markup())
        else:
            message = send_message(f"Your money: {user.money} 💵\nAvailable X skins:", user.id, None)
            edit_message(
                f"Your money: {user.money} 💵\nAvailable X skins:",
                user.id,
                x_skin_shop_markup(x_skins_in_shop, message.message_id),
                message.message_id
            )
    elif data == "o_shop":
        o_skins_in_shop = user_service.get_o_skin_shop_for_user(user)
        if len(o_skins_in_shop) == 0:
            send_message(O_SKIN_SHOP_EMPTY_MSG, user.id, base_markup())
        else:
            message = send_message(f"Your money: {user.money} 💵\nAvailable O skins:", user.id, None)
            edit_message(
                f"Your money: {user.money} 💵\nAvailable O skins:",
                user.id,
                o_skin_shop_markup(o_skins_in_shop, message.message_id),
                message.message_id
            )
    elif data.startswith("buy_x"):
        x_skin_id, message_id = map(int, data.split(" ")[1:])
        left_money = user_service.buy_x_skin(x_skin_id, user)
        if left_money < 0:
            send_message(f"You don't have enough money({-left_money} 💵)", user.id, base_markup())
        else:
            send_message(SKIN_ADDED_TO_COLLECTION, user.id, base_markup())
        delete_message(user.id, message_id)
    elif data.startswith("buy_o"):
        o_skin_id, message_id = map(int, data.split(" ")[1:])
        left_money = user_service.buy_o_skin(o_skin_id, user)
        if left_money < 0:
            send_message(f"You don't have enough money({-left_money} 💵)", user.id, base_markup())
        else:
            send_message(SKIN_ADDED_TO_COLLECTION, user.id, base_markup())
        delete_message(user.id, message_id)



bot.infinity_polling()
