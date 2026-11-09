from pico2d import *
import game_framework
import play_mode
import items

image = None


def init():
    global image
    image = load_image('item_select.png')


def finish():
    global image
    image = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return


def update():
    pass


def render():
    play_mode.render()
