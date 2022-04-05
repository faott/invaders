import pygame

WIDTH, HEIGHT = 800,600

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GRAY = (100,100,100)
ORANGE = (242, 90, 15)
SPACE_BLUE = (2,32,59)

colours_list = [WHITE, BLACK, RED, GREEN, BLUE, GRAY, ORANGE]

enemy__icon_small = [
    "media/enemy1_30.png",
    "media/enemy2_30.png",
    "media/enemy3_30.png",
    "media/enemy4_30.png",
]

enemy__icon_boss = [
    "media/enemy/boss_1_200.png",
    "media/enemy/boss_2_200.png",
]


font_types = {
    'uroob':"font/Uroob-Regular.ttf",
    'anarchonaut':"font/AnachronautRegular-5VRB.ttf"
}

icons = {
    'mute':"media/icon/mute.png",
    'settings':"media/icon/settings.png",
    'information':"media/icon/information.png",
}

player_icon = {

    'default': "media/player/player1_50.png",
    'player1_50': "media/player/player1_50.png",
    'player1_100':"media/player/player1_100.png",
    'player2_50': "media/player/player2_50.png",
    'player2_100':"media/player/player2_100.png",
}

explosion = {

    'enemy': "media/explosion/explosion.png",
    'player1': "media/explosion/player1_expl_100.png",
    'player2': "media/explosion/player2_expl_100.png",
}

background = {

    'start':"media/background0.png"
}



def get_text(text, size, colour=WHITE, type='uroob'):

    font = pygame.font.Font(font_types[type], size)
    surf = font.render(text, True, colour)

    return surf




