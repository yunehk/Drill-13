from pico2d import *
import game_framework
import game_world
from boy import Boy
from grass import Grass

boy = None


def init():
    global boy
    boy = Boy()
    game_world.add_oject(boy)
    game_world.add_oject(Grass(), 0)


def finish():
    global boy
    game_world.clear()
    boy = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            import title_mode
            game_framework.change_mode(title_mode)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not getattr(event, 'repeat', 0):
                import pause_mode
                game_framework.push_mode(pause_mode)
                return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            if not getattr(event, 'repeat', 0):
                import item_mode
                game_framework.push_mode(item_mode)
                return
        else:
            boy.handle_event(event)


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    global paused_at
    paused_at = get_time()


def resume():
    boy.idle_started_at += get_time() - paused_at

