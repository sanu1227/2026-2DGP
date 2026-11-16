import os

from pico2d import *
import game_framework
import game_world


class PauseMode:
    def __init__(self):
        self.font = None

    def init(self):
        self.font = load_font(
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'),
                         'Fonts', 'malgun.ttf'), 32)

    def finish(self):
        self.font = None

    def handle_events(self):
        for event in get_events():
            if event.type == SDL_QUIT:
                game_framework.quit()
                return
            elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
                game_framework.pop_mode()
                return

    def update(self):
        pass

    def render(self):
        clear_canvas()
        game_world.render()
        self.font.draw(252, 322, '정지 중 (P: 계속)', (0, 0, 0))
        self.font.draw(250, 324, '정지 중 (P: 계속)', (255, 255, 255))
        update_canvas()
