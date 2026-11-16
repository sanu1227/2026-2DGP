from pathlib import Path
import sys

from pico2d import *
import game_framework


image = None


def init():
    global image
    image = load_image(str(Path(__file__).with_name('title.png')))


def finish():
    global image
    image = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def update():
    pass


def render():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    update_canvas()


def pause():
    pass


def resume():
    pass


if __name__ == '__main__':
    open_canvas(800, 600)
    try:
        game_framework.run(sys.modules[__name__])
    finally:
        close_canvas()
