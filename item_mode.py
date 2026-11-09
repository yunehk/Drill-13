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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            choose_item(items.SMALL)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            choose_item(items.LARGE)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            choose_item(items.NONE)
            return
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_ESCAPE, SDLK_i):
            if not getattr(event, 'repeat', 0):
                game_framework.pop_mode()
                return
        elif event.type == SDL_KEYUP:
            play_mode.boy.handle_event(event)


def choose_item(item):
    play_mode.boy.selected_item = item
    game_framework.pop_mode()


def update():
    pass


def render():
    clear_canvas()
    play_mode.game_world.render()
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()
