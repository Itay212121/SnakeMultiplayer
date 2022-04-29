from tkinter.messagebox import NO
import pygame

snake_width = speed = 15


class Player:
    def __init__(self, username, game, color):
        self.username = username
        self.game = game
        self.spawn()
        game.add_player(self)
        self.score = 0
        self.color = color

    def spawn(self):
        self.vel = [speed, 0]  # going right
        self.snake = [[0, 40 * len(self.game.players)]]
        self.score = 0
        self.ready = False
