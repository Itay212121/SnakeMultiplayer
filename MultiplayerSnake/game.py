import pygame
from player import Player
import random
window_width = 1500
window_height = 800
snake_width = 15

i = 0


class Game:
    def __init__(self):
        self.ready = False
        self.players = []
        self.last_spawn = 0
        self.apples = []

    def update_server(self, n):
        n.send(self)

    def add_player(self, player):
        self.players.append(player)

    def update_players(self, player):
        new_players = []
        for i in self.players:
            if i.username == player.username:
                new_players.append(player)
            else:
                new_players.append(i)
        self.players = new_players

    def disconnect_player(self, username):
        new_players = []
        for i in self.players:
            if i.username != username:
                new_players.append(i)
        self.players = new_players

    def is_players_touching_apple(self, apple):
        is_in_snake = False
        for player in self.players:
            for part in player.snake:
                if part == apple:
                    is_in_snake = True
        return is_in_snake

    def spawn_apple(self):
        x, y = random.randint(
            1, window_width // snake_width) * snake_width, random.randint(1, window_height // snake_width) * snake_width

        if self.is_players_touching_apple([x, y]):
            self.spawn_apple()
        else:
            self.apples.append([x, y])

    def is_touching_apple(self, snake, apple):
        apple_x, apple_y = apple
        is_in_snake = False
        for part in snake:
            x, y = part
            print(abs(x - apple_x), abs(y - apple_y))
            if abs(x - apple_x) < snake_width and abs(y - apple_y) < snake_width:
                is_in_snake = True
        return is_in_snake
