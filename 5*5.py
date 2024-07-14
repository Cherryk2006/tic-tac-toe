
import telebot
from telebot import types
import random

API_TOKEN = "your-token"
bot = telebot.TeleBot('6773691989:AAFtKmympPtdYCMMO_pZp5B7EHo3LkgoZIU')

class Game:
    def __init__(self, user_x, user_o, message_id):
        self.root = [[0] * 5 for _ in range(5)]
        self.user_x = user_x
        self.user_o = user_o
        self.current_step = "x"
        self.game_over = False
        self.message_id = message_id

    def check_win(self):
        def check_line(line):
            count_x = 0
            count_o = 0
            for cell in line:
                if cell == 1:
                    count_x += 1
                    count_o = 0
                elif cell == 2:
                    count_o += 1
                    count_x = 0
                else:
                    count_x = 0
                    count_o = 0

                if count_x == 4:
                    return 1
                if count_o == 4:
                    return 2
            return 0

        # Check rows and columns
        for i in range(5):
            if check_line(self.root[i]) in [1, 2]:
                return check_line(self.root[i])
            if check_line([self.root[j][i] for j in range(5)]) in [1, 2]:
                return check_line([self.root[j][i] for j in range(5)])

        # Check diagonals
        for i in range(2):
            if check_line([self.root[i + j][j] for j in range(5 - i)]) in [1, 2]:
                return check_line([self.root[i + j][j] for j in range(5 - i)])
            if check_line([self.root[j][i + j] for j in range(5 - i)]) in [1, 2]:
                return check_line([self.root[j][i + j] for j in range(5 - i)])
            if check_line([self.root[4 - (i + j)][j] for j in range(5 - i)]) in [1, 2]:
                return check_line([self.root[4 - (i + j)][j] for j in range(5 - i)])
            if check_line([self.root[4 - j][i + j] for j in range(5 - i)]) in [1, 2]:
                return check_line([self.root[4 - j][i + j] for j in range(5 - i)])

        return 0

    def make_move(self, x, y):
        if self.game_over or self.root[x][y] != 0:
            return False
        if self.current_step == "x":
            self.root[x][y] = 1
            self.current_step = "o"
        else:
            self.root[x][y] = 2
            self.current_step = "x"
        if self.check_win():
            self.game_over = True
        return True


bot.infinity_polling()
