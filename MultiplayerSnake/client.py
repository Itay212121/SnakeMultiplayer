
import pygame
import pickle
from network import Network
FPS = 30
width = 1500
height = 800

snake_width = speed = 15
GAME_FPS = speed * 1.5
apple_delay = 100


def is_dead(snake):

    snake_copy = []
    for part in snake:
        x, y = part
        if part in snake_copy:
            return True
        if x > width or y > height or x < 0 or y < 0:
            return True

        snake_copy.append(part)

    return False


def draw_scoreboard(win, all_players, player):
    font = pygame.font.SysFont("calibri", 20)
    score_board_text = font.render(
        "Scoreboard:", 1, (0, 0, 0))
    win.blit(score_board_text, (width - score_board_text.get_width() - 10, 40))

    by_score = sorted(all_players, key=lambda p: p.score)
    for i in range(0, len(by_score)):
        curr_player = by_score[::-1][i]

        score_text = font.render(
            str(i + 1) + ". " + curr_player.username + ", " + str(curr_player.score) + " points", 1, curr_player.color)
        win.blit(score_text, (width - score_text.get_width() -
                 10, 40 + ((i + 1) * 30)))
        if player.username == curr_player.username:
            pygame.draw.rect(win, (0, 0, 0), (width - score_text.get_width() - 15,
                             35 + ((i + 1) * 30), score_text.get_width() + 5, score_text.get_height() + 5), width=2)


def redrawWindow(win, game, apples, this_player):

    win.fill((255, 255, 255))
    for player in game.players:
        for part in player.snake:
            x, y = part
            pygame.draw.rect(win, player.color,
                             (x, y, snake_width, snake_width))

    for apple in apples:
        x, y = apple
        pygame.draw.rect(win, (0, 255, 0),
                         (x, y, snake_width, snake_width))

    draw_scoreboard(win, game.players, this_player)

    pygame.display.update()


def move(snake, vel):
    for i in range(len(snake) - 1):
        snake[len(snake) - i - 1] = snake[len(snake) - i - 2]
    snake[0] = [snake[0][0] + vel[0], snake[0][1] + vel[1]]


def main(win, network, game, player):

    run = True
    clock = pygame.time.Clock()
    last = None
    while run:
        try:
            game = network.send("game")
            if not game.ready:
                player.spawn()
                main_menu(win, network, player)
                print("not ready")
                return
            redrawWindow(win, game, game.apples, player)

            clock.tick(GAME_FPS)
            if is_dead(player.snake):
                player.spawn()

            for apple in game.apples:
                if game.is_touching_apple(player.snake, apple):
                    network.send(apple)
                    player.score += 1
                    last = player.snake[-1]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    last = player.snake[-1]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.vel = [-1 * speed, 0]
                    if event.key == pygame.K_RIGHT:
                        player.vel = [speed, 0]
                    if event.key == pygame.K_UP:
                        player.vel = [0, -1 * speed]
                    if event.key == pygame.K_DOWN:
                        player.vel = [0, speed]
            move(player.snake, player.vel)
            if last != None:
                player.snake.append(last)
                last = None
            network.send(player)
        except Exception as e:
            print(e)
            run = False

    network.send("delete-player|" + player.username)
    network.send(player)


def redrawMenu(win, player, all_players):
    win.fill((160, 160, 160))
    font = pygame.font.SysFont("calibri", 50)
    ready_font = pygame.font.SysFont("calibri", 80)

    username_text = font.render(
        "Your username is: " + player.username, 1, (0, 0, 0))
    win.blit(username_text, (width / 2 - username_text.get_width() / 2, 50))

    text = font.render("Joined Players: ", 1, (0, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, 150))

    for i in range(len(all_players)):
        curr_player = all_players[i]
        if curr_player.ready:
            text = font.render(str(i + 1) + ". " +
                               all_players[i].username, 1, (0, 255, 0))
        else:
            text = font.render(str(i + 1) + ". " +
                               all_players[i].username, 1, (255, 0, 0))

        win.blit(text, (width / 2 - text.get_width() / 2, 150 + (i + 1) * 60))

     # Ready button

    readyButtonWidth = 610
    readyButtonHeight = 115

    readyButtonX = win.get_width() // 2 - readyButtonWidth // 2
    readyButtonY = 600

    readyBtn = pygame.draw.rect(win, (0, 0, 0), (readyButtonX, readyButtonY, readyButtonWidth, readyButtonHeight),
                                width=4)
    btntext = "Ready"
    if player.ready:
        btntext = "Unready"

    text = ready_font.render(btntext, 1, (0, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, 620))

    pygame.display.update()

    return readyBtn


def gameReady(all_players):
    if len(all_players) <= 1:
        return False

    for p in all_players:
        if not p.ready:
            return False
    return True


def main_menu(win, network, player):
    pygame.font.init()

    run = True
    clock = pygame.time.Clock()

    while run:
        try:
            all_players = network.send(player)

            readyBtn = redrawMenu(win, player, all_players)
            if gameReady(all_players):
                run = False

            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if (x >= readyBtn.x and x <= (readyBtn.width + readyBtn.x)) and (y >= readyBtn.y and y <= (readyBtn.height + readyBtn.y)):

                        if (player.ready) or (not player.ready and len(all_players) >= 2):
                            player.ready = not player.ready

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        except:
            return
    game = network.send("game_ready")
    main(win, network, game, player)
    print("cock")


if __name__ == '__main__':
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client")

    network = Network()
    player = pickle.loads(network.get())

    main_menu(win, network, player)
