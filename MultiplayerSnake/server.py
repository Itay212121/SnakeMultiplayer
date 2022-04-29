
import socket
import threading
import pickle
import random

from game import Game
from player import Player
import datetime
usernames = ["ProFornitePlayer", "Ninja",
             "IKilledYouBozo", "TheSnakeEater", "PickachuIsCute"]

colors = [(120, 120, 120), (255, 0, 0), (0, 120, 120), (0, 0, 255), (0, 0, 0)]
apple_spawn_rate = 5


def get_username(current_players):

    if len(current_players) >= len(usernames):
        return -1

    username = random.choice(usernames)
    if username in [i.username for i in current_players]:
        return get_username(current_players)
    return username


def get_color(current_players):
    if len(current_players) >= len(colors):
        return -1

    color = random.choice(colors)
    if color in [i.color for i in current_players]:
        return get_color(current_players)
    return color


def handle_input(data, game, conn, player):
    this_player = player
    if type(data) == Player:
        game.update_players(data)
        conn.send(pickle.dumps(game.players))

    elif data == "game_ready":
        game.ready = True
        game.last_spawn = datetime.datetime.now()
        conn.send(pickle.dumps(game))

    elif data == "game":
        conn.send(pickle.dumps(game))

    elif type(data) == Game:
        game = data
        conn.send(pickle.dumps(game))

    elif type(data) == list:
        game.apples.remove(data)
        conn.send(pickle.dumps(game))

    elif data.startswith("delete-player"):
        game.disconnect_player(data.split("|")[1])
        conn.send(pickle.dumps("accepted"))
        return None

    return this_player


def threaded_client(conn, game):

    generated_username = get_username(game.players)
    if generated_username == -1:
        conn.close()
        return

    this_player = Player(generated_username, game, get_color(game.players))

    conn.send(pickle.dumps(this_player))
    while this_player != None:

        if len(game.players) <= 1:
            game.ready = False

        if game.last_spawn == 0 or (datetime.datetime.now() - game.last_spawn).seconds >= apple_spawn_rate:
            game.last_spawn = datetime.datetime.now()
            game.spawn_apple()

        client_data = pickle.loads(conn.recv(8192))

        handle_input(client_data, game, conn, this_player)

    conn.close()


def main():
    server = "10.0.0.14"

    port = 6003
    game = Game()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(e)
        return 0

    s.listen(5)
    print("Waiting for a connection, Server Started")

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        thread = threading.Thread(target=threaded_client, args=(conn, game))
        thread.start()


if __name__ == "__main__":
    main()
