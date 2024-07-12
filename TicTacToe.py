import telebot
from telebot import types
import random

API_TOKEN = "your-token"
bot = telebot.TeleBot('6773691989:AAFtKmympPtdYCMMO_pZp5B7EHo3LkgoZIU')

class Game:

    def __init__(self, user_x, user_o, message_id):
        # 0 - empty cell; 1 - x; 2 - y.
        self.root = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.user_x = user_x
        self.user_o = user_o
        self.current_step = "x"
        self.game_over = False
        self.message_id = message_id

    def check_win(self):
        count_empty_cell = 0
        for y in range(0, 3):
            line = ""
            for x in range(0, 3):
                if self.root[y][x] == 0:
                    count_empty_cell += 1
                line += str(self.root[y][x])
            if line == "111":
                self.game_over = True
                return [1, (y, 0), (y, 1), (y, 2)]
            if line == "222":
                self.game_over = True
                return [2, (y, 0), (y, 1), (y, 2)]
        for x in range(0, 3):
            line = ""
            for y in range(0, 3):
                line += str(self.root[y][x])
            if line == "111":
                self.game_over = True
                return [1, (0, x), (1, x), (2, x)]
            if line == "222":
                self.game_over = True
                return [2, (0, x), (1, x), (2, x)]
        line = ""
        for i in range(0, 3):
            line += str(self.root[i][i])
        if line == "111":
            self.game_over = True
            return [1, (0, 0), (1, 1), (2, 2)]
        if line == "222":
            self.game_over = True
            return [2, (0, 0), (1, 1), (2, 2)]
        line = ""
        for i in range(0, 3):
            line += str(self.root[2 - i][i])
        if line == "111":
            self.game_over = True
            return [1, (2, 0), (1, 1), (0, 2)]
        if line == "222":
            self.game_over = True
            return [2, (2, 0), (1, 1), (0, 2)]

        if count_empty_cell == 0:
            self.game_over = True
            return 0
        return -1

    def next_step(self, x, y):
        if self.current_step == "x":
            self.root[y][x] = 1
            winner = self.check_win()
            if winner != -1:
                return winner
            self.current_step = "o"
        elif self.current_step == "o":
            self.root[y][x] = 2
            winner = self.check_win()
            if winner != -1:
                return winner
            self.current_step = "x"
        self.user_x.my_step = not self.user_x.my_step
        self.user_o.my_step = not self.user_o.my_step
        return -1


class User:

    def __init__(self, user_id, first_name):
        self.game = None
        self.user_id = user_id
        self.friend = None
        self.role = None
        self.first_name = first_name
        self.my_step = False
        self.message_id = -1

    def set_friend(self, friend):
        self.friend = friend

    def start_new_game(self, message_id):
        if random.randint(0, 1) == 0:
            self.role = "❌"
            self.friend.role = "⭕"
            self.my_step = True
            self.friend.my_step = False
            self.game = Game(self, self.friend, message_id)
        else:
            self.role = "⭕"
            self.friend.role = "❌"
            self.my_step = False
            self.friend.my_step = True
            self.game = Game(self.friend, self, message_id)
        self.friend.game = self.game


users = {}

def print_matrix(matrix):
    output = ""
    for line in matrix:
        for el in line:
            if el == 0:
                output += "⬜"
            elif el == 1:
                output += "❌"
            else:
                output += "⭕"
        output += "\n"
    return output

def print_winner_matrix(matrix, data):
    output = ""
    character = ""
    for y in range(0, 3):
        for x in range(0, 3):
            if matrix[y][x] == 0:
                matrix[y][x] = "⬜"
            elif matrix[y][x] == 1:
                matrix[y][x] = "❌"
            else:
                matrix[y][x] = "⭕"
    if data[0] == 1:
        character = "❎"
    else:
        character = "🟢"
    matrix[data[1][0]][data[1][1]] = character
    matrix[data[2][0]][data[2][1]] = character
    matrix[data[3][0]][data[3][1]] = character
    for line in matrix:
        for el in line:
            output += el
        output += "\n"
    return output

def get_markup(matrix, user_id):
    markup = types.InlineKeyboardMarkup()
    for y in range(0, 3):
        lst = []
        for x in range(0, 3):
            if matrix[y][x] == 0:
                lst.append(types.InlineKeyboardButton(text="⬜", callback_data=f"{y} {x} {user_id}"))
            elif matrix[y][x] == 1:
                lst.append(types.InlineKeyboardButton(text="❌", callback_data=f"none"))
            elif matrix[y][x] == 2:
                lst.append(types.InlineKeyboardButton(text="⭕", callback_data=f"none"))
        markup.row(lst[0], lst[1], lst[2])
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    users[message.from_user.id] = User(message.from_user.id, message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start game")
    btn2 = types.KeyboardButton("Show my id")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Hi I'm Tic Toe BOT. And here you can play Tic Toe with your friends.",
                     reply_markup=markup)
    print(users)

@bot.message_handler(commands=["invite"])
def invite(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start game")
    btn2 = types.KeyboardButton("Show my id")
    markup.add(btn1, btn2)
    friend_id = int(message.text.split(" ")[1])
    user_id = message.from_user.id

    user = users[user_id]
    friend = users[friend_id]
    user.set_friend(friend)
    friend.set_friend(user)
    print(users)
    bot.send_message(user_id, text=f"You are connected to friend {friend.first_name}", reply_markup=markup)
    bot.send_message(friend_id, text=f"You are connected to friend {user.first_name}", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Show my id":
        print(message.id)
        bot.send_message(message.chat.id, text=f"{message.from_user.id}")
    if message.text == "Start game":
        user = users[message.from_user.id]
        if user.friend is None:
            bot.send_message(message.chat.id,
                             text="Set your friend's id using the /invite command (for example: /invite 58478393)")
        friend = user.friend
        user.start_new_game(message.id + 1)

        if user.my_step:
            markup = get_markup(user.game.root, user.user_id)
            user_message = bot.send_message(user.user_id, text=f"👉{user.role}{user.first_name}\n  {friend.role}{friend.first_name}", reply_markup=markup)
            friend_message = bot.send_message(friend.user_id, text=f"👉{user.role}{user.first_name}\n  {friend.role}{friend.first_name}")
            print(user_message.id)
            user.message_id = user_message.id
            print(friend_message.id)
            friend.message_id = friend_message.message_id
        else:
            markup = get_markup(user.game.root, friend.user_id)
            user_message = bot.send_message(user.user_id, text=f"  {user.role}{user.first_name}\n👉{friend.role}{friend.first_name}")
            friend_message = bot.send_message(friend.user_id, text=f"  {user.role}{user.first_name}\n👉{friend.role}{friend.first_name}", reply_markup=markup)
            print(user_message.id)
            user.message_id = user_message.id
            print(friend_message.id)
            friend.message_id = friend_message.message_id


@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "none":
        return -1
    y, x, user_id = map(int, callback.data.split(" "))
    user = users[user_id]
    friend = user.friend
    game = user.game
    if game.game_over:
        return -1
    winner = game.next_step(x, y)
    if winner == -1:
        markup = get_markup(game.root, friend.user_id)
        bot.edit_message_text(text=f"  {user.role}{user.first_name}\n👉{friend.role}{friend.first_name}", chat_id=user.user_id, message_id=user.message_id)
        bot.edit_message_text(text=f"  {user.role}{user.first_name}\n👉{friend.role}{friend.first_name}", chat_id=friend.user_id, message_id=friend.message_id, reply_markup=markup)
    elif winner == 0:
        bot.edit_message_text(text=f"⚖️{user.role}{user.first_name}\n⚖️{friend.role}{friend.first_name}\nIt's a draw:\n{print_matrix(game.root)}", chat_id=user.user_id, message_id=user.message_id)
        bot.edit_message_text(text=f"⚖️{user.role}{user.first_name}\n⚖️{friend.role}{friend.first_name}\nIt's a draw:\n{print_matrix(game.root)}", chat_id=friend.user_id, message_id=friend.message_id)
    elif winner[0] == 1:

        if user.role == "❌":
            user_status = "🏆"
            friend_status = "🤕"
            winner_name = user.first_name
        else:
            user_status = "🤕"
            friend_status = "🏆"
            winner_name = friend.first_name
        output = print_winner_matrix(game.root, winner)
        bot.edit_message_text(
            text=f"{user_status}{user.role}{user.first_name}\n{friend_status}{friend.role}{friend.first_name}\n{winner_name} is winner:\n{output}",
            chat_id=user.user_id, message_id=user.message_id)
        bot.edit_message_text(
            text=f"{user_status}{user.role}{user.first_name}\n{friend_status}{friend.role}{friend.first_name}\n{winner_name} is winner:\n{output}",
            chat_id=friend.user_id, message_id=friend.message_id)
    elif winner[0] == 2:

        if user.role == "⭕":
            user_status = "🏆"
            friend_status = "🤕"
            winner_name = user.first_name
        else:
            user_status = "🤕"
            friend_status = "🏆"
            winner_name = friend.first_name
        output = print_winner_matrix(game.root, winner)
        bot.edit_message_text(
            text=f"{user_status}{user.role}{user.first_name}\n{friend_status}{friend.role}{friend.first_name}\n{winner_name} is winner:\n{output}",
            chat_id=user.user_id, message_id=user.message_id)
        bot.edit_message_text(
            text=f"{user_status}{user.role}{user.first_name}\n{friend_status}{friend.role}{friend.first_name}\n{winner_name} is winner:\n{output}",
            chat_id=friend.user_id, message_id=friend.message_id)





bot.infinity_polling()
