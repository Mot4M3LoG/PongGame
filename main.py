"""
This program enables up to 2 users to play the old game "pong".

Program contains welcome screen with mode-choosing option,
counts score of a player or both players at once, has collision detection
and mouse position detection.
in one player game, ball speeds up after 5 points, then in 2 player game
the game is held until any of players reaches 9 points, which displays
the winner and closes the program after a few seconds.
"""
import pygame
import sys
import random


def one_player(b, p, vector, counter):
    """
    this function handles one player game, all moves of ball and paddle,
    as well as collisions ball-paddle, ball-window and paddle-window.

    Function takes parameters of ball(b) and paddle(p) (position and size)
    vector of movement of the ball, and counter, to get to know when
    to increase the ball's speed (indication of player doing well)

    In each iteration, function returns ball and paddle change of position
    checks collisions and displays it onto generated screen.
    """
    global score_1   # this value is used in different places, hence global
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # managing quit and movement
                sys.exit()                 # conditions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p = p.move(0, -step)
                if event.key == pygame.K_DOWN:
                    p = p.move(0, step)

        if score_1 == 5:
            while counter < 1:   # "increase of game's difficulty"
                vector[0] = vector[0] * 2
                vector[1] = vector[1] * 2
                counter += 1

        if p.bottom > win.bottom:
            p.bottom = win.bottom  # window-paddle collision
        if p.top < win.top:
            p.top = win.top

        b = b.move(vec)
        if b.left < win.left:
            vec[0] = -vec[0]   # ball movement, point management and lose
            stop(score_1)      # condition
        if b.right > win.right:
            vec[0] = -vec[0]
            score_1 = int(score_1)
            score_1 = score_1 + 1
        if b.top < win.top or b.bottom > win.bottom:
            vec[1] = -vec[1]

        collide(p, b)

        scr.fill(black)
        pygame.draw.rect(scr, white, p)
        pygame.draw.rect(scr, white, b)   # screen updates
        score(score_1)
        pygame.display.flip()
        fps.tick(260)


def two_player(p1, p2, b, left_points, right_points, vector):
    """
    this function handles two player game, all moves of ball and paddles,
    as well as collisions ball-paddles, ball-window and paddles-window.

    Function takes parameters of ball(b) and paddles(p1 - left, p2 - right)
    (position and size), displays left and right player's points using
    another function and vector of movement of the ball.

    In each iteration, function returns ball and paddles changes of position,
    checks collisions and displays it onto generated screen, while keeping
    track if the game should end (any player reaching 9 points) and handles
    displaying the winner's side.
    """
    global color
    global rgb
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keyboard_check = pygame.key.get_pressed()  # this type handles all key
        if keyboard_check[pygame.K_UP]:  # pressings at once, hence in this way
            p2 = p2.move(0, -step)
        if keyboard_check[pygame.K_DOWN]:
            p2 = p2.move(0, step)
        if keyboard_check[pygame.K_w]:
            p1 = p1.move(0, -step)
        if keyboard_check[pygame.K_s]:
            p1 = p1.move(0, step)

        if p1.bottom > win.bottom:
            p1.bottom = win.bottom
        if p1.top < win.top:
            p1.top = win.top
        if p2.bottom > win.bottom:
            p2.bottom = win.bottom
        if p2.top < win.top:
            p2.top = win.top

        b = b.move(vector)
        if b.left < win.left:
            right_points += 1  # point management and round reset
            message = "Right player gets the point!"
            b = pygame.Rect(0, 0, 30, 30)
            b.center = win.center
            p1 = pygame.Rect(0, 0, 30, 100)
            p1.midleft = win.midleft
            p2 = pygame.Rect(0, 0, 30, 100)
            p2.midright = win.midright
            point_scored(message, vector)

        if b.right > win.right:
            left_points += 1   # point management and round reset
            message = "Left player gets the point!"
            b = pygame.Rect(0, 0, 30, 30)
            b.center = win.center
            p1 = pygame.Rect(0, 0, 30, 100)
            p1.midleft = win.midleft
            p2 = pygame.Rect(0, 0, 30, 100)
            p2.midright = win.midright
            point_scored(message, vector)

        if b.top < win.top or b.bottom > win.bottom:
            vec[1] = -vec[1]
            rgb = random.randint(0, 0xFFFFFFFF)
            color = pygame.color.Color(rgb)

        collide(p1, b, p2)

        scr.fill(black)
        pygame.draw.rect(scr, white, p1)
        pygame.draw.rect(scr, white, p2)
        pygame.draw.rect(scr, color, b, 5)
        score_2_players(left_points, right_points)
        fps.tick(325)
        pygame.display.flip()

        if left_points == 9:   # game is played until either of players
            goodbye2 = firstfont.render("Left player won the game!", True,
                                        "red")  # reaches 9 points
            goodbye2_box = goodbye2.get_rect()
            goodbye2_box.center = win.center
            scr.fill(black)
            scr.blit(goodbye2, goodbye2_box)
            score_2_players(left_points, right_points)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit()

        if right_points == 9:  # same here, but different player
            scr.fill(black)
            goodbye2 = firstfont.render("Right player won the game!", True,
                                        "red")
            goodbye2_box = goodbye2.get_rect()
            goodbye2_box.center = win.center
            scr.fill(black)
            scr.blit(goodbye2, goodbye2_box)
            score_2_players(left_points, right_points)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit()


def score(points):
    """
    this function handles score parameter in single player game, as well as
    displaying it onto the screen.

    Function takes only parameter, points, which is how many times the player
    managed to keep the ball out of his "goal zone"

    In each iteration, function displays how many points the player has on the
    screen in red color.
    """
    points = str(points)  # just displaying points
    main_score = firstfont.render(points, True, "red")
    main_score_box = main_score.get_rect()
    main_score_box.center = ((win.center[0] / 2) * 3, win.center[1] / 2)
    scr.blit(main_score, main_score_box)


def score_2_players(points_left, points_right):
    """
    this function handles score parameter in two player game, as well as
    displaying it onto the screen.

    Function takes two parameters, points of corresponding players, which are
    used to keep track of game's progress, and keep players informed.

    In each iteration, function returns how many points each player has on
    their own side
    """
    divider = pygame.Rect(win.centerx - 10, 0, 20, 70)
    pygame.draw.rect(scr, blue, divider)
    left_player = firstfont.render(str(points_left), True, "red")
    left_player_box = left_player.get_rect()  # only displays
    left_player_box.center = (win.centerx - 40, 0 + 40)
    right_player = firstfont.render(str(points_right), True, "red")
    right_player_box = right_player.get_rect()
    right_player_box.center = (win.centerx + 40, 0 + 40)
    scr.blit(left_player, left_player_box)
    scr.blit(right_player, right_player_box)
    int(points_left)
    int(points_right)


def collide(paddle1, ball_mov, paddle2=None):
    """
    this function handles collisions in both game modes.

    Function takes positions of paddle and a ball (or 2 paddles in 2 player
    game), then compares them to see, if any vector requires changing.

    In each iteration, function returns positions of objects,
    and changes direction of ball if it collides with a paddle.
    """
    global rgb
    global color
    if paddle2 is None:
        c = pygame.Rect.colliderect(paddle1, ball_mov)
        if c:  # collision handling for left paddle onky
            if (abs(ball_mov.bottom - paddle1.top)
                    < abs(ball_mov.left - paddle1.right)) or \
                        (abs(ball_mov.top - paddle1.bottom)
                         < abs(ball_mov.left - paddle1.right)):
                vec[1] = -vec[1]
            else:
                vec[0] = -vec[0]
    elif paddle2 is not None:  # collision handling for left AND right paddle
        c = pygame.Rect.colliderect(paddle1, ball_mov)
        if c:
            if (abs(ball_mov.bottom - paddle1.top)
                < abs(ball_mov.left - paddle1.right)) or \
                        (abs(ball_mov.top - paddle1.bottom)
                         < abs(ball_mov.left - paddle1.right)):
                vec[1] = -vec[1]
            else:
                vec[0] = -vec[0]
                rgb = random.randint(0, 0xFFFFFFFF)
                color = pygame.color.Color(rgb)
        d = pygame.Rect.colliderect(paddle2, ball_mov)
        if d:
            if (abs(ball_mov.bottom - paddle2.top)
                < abs(ball_mov.right - paddle2.left)) or \
                     (abs(ball_mov.top - paddle2.bottom)
                      < abs(ball_mov.right - paddle2.left)):
                vec[1] = -vec[1]
            else:
                vec[0] = -vec[0]
                rgb = random.randint(0, 0xFFFFFFFF)
                color = pygame.color.Color(rgb)


def stop(player_score):
    """
    this function handles the situation, in which player loses the one player
    game. displays number of points and a message, then exits after few
    seconds.

    Function only takes player's score, to pass it onto the screen

    (after ball touches player's "goal zone") it returns "goodbye" screen
    saying good game asnwell as number of points player has at the end,
    then exits the program.
    """
    player_score = str(player_score)
    goodbye = firstfont.render("Good Game!", True, "red")
    goodbye_box = goodbye.get_rect()  # stop game and display some messages
    goodbye_box.center = (win.center[0], win.center[1] / 2)
    score_disp = firstfont.render(player_score, True, "red")
    score_disp_box = score_disp.get_rect()
    score_disp_box.center = win.center
    scr.fill(black)
    scr.blit(score_disp, score_disp_box)
    scr.blit(goodbye, goodbye_box)
    pygame.display.flip()
    pygame.time.wait(5000)
    sys.exit()


def point_scored(sign, vector):
    """
    this function handles situation in 2 player game, in which one of the
    players manages to get a point (other player doesn't hit the ball in time)

    Function takes sign as a message, which is displayed on the screen,
    indicating which player scored the point, and vector, to pass it to
    other function (generate_ball_movement).

    In each iteration, function checks if any player scored a point, and
    displays which one if this event occurs.
    """
    score_disp = firstfont.render(sign, True, "red")
    score_disp_box = score_disp.get_rect()
    score_disp_box.center = win.center  # some displays
    scr.blit(score_disp, score_disp_box)
    generate_ball_movement(vector)
    pygame.display.flip()
    pygame.time.wait(1500)


def mouse_cursor(rect, m_pos):
    """
    this function checks mouse's position before any of game modes start, 
    as well as collisions with rectangles(mode choices).

    Function takes rect as position of a rectangle, which is used to select
    the game mode, and position of the mouse as x and y.

    In each iteration before game starts, returns if mouse touches any of 
    rectangles(mode choices)
    """
    pygame.event.get()
    if rect.collidepoint(m_pos[0], m_pos[1]):
        return True
    else:
        return False


def generate_ball_movement(vector):
    """
    this function, in 2 player game, randomizes ball's starting movement, after
    any of the players scored a point. 

    function takes only vector, to then modify it a little
    (unpredictable ball movement)

    returns different vector value, after any of players scores a point
    """
    x = random.randint(0, 3)
    if x == 0:
        pass
    elif x == 1:
        vector[0] = vector[0] * (-1)
    elif x == 2:
        vector[1] = vector[1] * (-1)
    elif x == 3:
        vector[0] = vector[0] * -1
        vector[1] = vector[1] * -1


def g_setup():
    """
    this function sets up all necessary values of welcome screen and mode
    choosing.

    takes no parameters

    returns rectangles of mode choice, a welcome message and instruction how
    to choose certain mode.
    """
    welcome_sign = firstfont.render("Welcome!", True, "red")
    welcome_sign_box = welcome_sign.get_rect()
    welcome_sign_box.center = (win.center[0], win.center[1] / 2)
    mode_choice = secondfont.render(
            "hover mouse over BLUE box for 1-player pong, "
            "and GREEN for 2-player", True, "red")
    mode_choice_box = mode_choice.get_rect()
    mode_choice_box.center = (win.center[0], win.center[1] / (4 / 3))
    scr.blit(welcome_sign, welcome_sign_box)
    scr.blit(mode_choice, mode_choice_box)
    pygame.draw.rect(scr, blue, choice_1)
    pygame.draw.rect(scr, green, choice_2)
    pygame.display.flip()


# ----- INITIALIZATION AND VARIABLES -----
if __name__ == "__main__":
    black = (0, 0, 0)    # bunch of colors
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    rgb = random.randint(0, 0xFFFFFFFF)
    color = pygame.color.Color(rgb)
    pygame.init()
    pygame.key.set_repeat(25, 25)
    fps = pygame.time.Clock()
    scr = pygame.display.set_mode((1400, 720))
    win = scr.get_rect()
    fps.tick(260)

    count = 0
    score_1 = score_right = score_left = 0

    firstfont = pygame.font.Font('freesansbold.ttf', 65)
    secondfont = pygame.font.Font('freesansbold.ttf', 25)

    # choice_1 and 2 are rectangles, which correspond to different game modes
    # (one or two player)
    choice_1 = pygame.Rect(win.center[0] / 2, (win.center[1] / 2) * 3, 40, 40)
    choice_2 = pygame.Rect((win.center[0] / 2) * 3, ((win.center[1] / 2) * 3),
                           40, 40)

    # ------ END OF INITIALIZATION ------

    while True:
        m_position = pygame.mouse.get_pos()  # gets mouse position
        g_setup()
        if mouse_cursor(choice_1, m_position):
            step = 8   # paddle movement
            vec = [1, 1]  # ball movement
            ball = pygame.Rect(0, 0, 30, 30)
            ball.center = win.center
            paddle = pygame.Rect(0, 0, 30, 100)
            paddle.midleft = win.midleft
            pygame.display.flip()
            generate_ball_movement(vec)
            pygame.time.wait(700)  # just for players to get ready
            one_player(ball, paddle, vec, count)  # start the game
        elif mouse_cursor(choice_2, m_position):
            step = 1   # almost the same here, but different values
            vec = [1, 1]
            ball = pygame.Rect(0, 0, 30, 30)
            ball.center = win.center
            paddle_left = pygame.Rect(0, 0, 30, 100)
            paddle_left.midleft = win.midleft
            paddle_right = pygame.Rect(0, 0, 30, 100)
            paddle_right.midright = win.midright
            pygame.display.flip()
            generate_ball_movement(vec)
            pygame.time.wait(700)
            two_player(paddle_left, paddle_right, ball, score_left, score_right,
                       vec)
