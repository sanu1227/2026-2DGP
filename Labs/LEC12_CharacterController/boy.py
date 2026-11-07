from pico2d import (load_image, get_canvas_width, SDL_KEYDOWN, SDL_KEYUP,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE)
from transitions import Machine
from math import pi, sin
from time import monotonic

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.run_keys = []
        self.sleep_progress = 0
        self.reset_idle()
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.last_update = monotonic()
        self.machine = Machine(model=self, states=['IDLE', 'SLEEP', 'RUN'], initial='IDLE',
                               auto_transitions=False)
        self.machine.add_transition('idle', 'IDLE', None, after='update_idle')
        self.machine.add_transition('sleep', 'IDLE', 'SLEEP')
        self.machine.add_transition('wake', 'SLEEP', 'IDLE', after='reset_idle')
        self.machine.add_transition('run', ['IDLE', 'SLEEP'], 'RUN')
        self.machine.add_transition('stop', 'RUN', 'IDLE', after='reset_idle')

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and self.state == 'SLEEP':
            self.wake()
        elif (event.type in (SDL_KEYDOWN, SDL_KEYUP)
              and event.key in (SDLK_LEFT, SDLK_RIGHT)):
            if event.type == SDL_KEYDOWN and event.key not in self.run_keys:
                self.run_keys.append(event.key)
            elif event.type == SDL_KEYUP and event.key in self.run_keys:
                self.run_keys.remove(event.key)
            if self.run_keys:
                if self.state != 'RUN':
                    self.run()
            elif self.state == 'RUN':
                self.stop()

    def reset_idle(self):
        self.idle_since = monotonic()

    def update(self):
        now = monotonic()
        dt = now - self.last_update
        step = dt / 0.4
        self.last_update = now
        self.sleep_progress = max(0, min(1, self.sleep_progress +
                                        (step if self.state == 'SLEEP' else -step)))
        if self.state == 'IDLE':
            if self.sleep_progress == 0:
                self.idle()
            if now - self.idle_since >= 5:
                self.sleep()
        elif self.state == 'RUN' and self.sleep_progress == 0:
            self.face_dir = 1 if self.run_keys[-1] == SDLK_RIGHT else -1
            self.x = max(50, min(get_canvas_width() - 50, self.x + self.face_dir * 200 * dt))
            self.frame = (self.frame + 1) % 8

    def update_idle(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        row = 300 if self.face_dir == 1 else 200
        if self.sleep_progress > 0:
            progress = self.sleep_progress
            progress = progress * progress * (3 - 2 * progress)
            angle = self.face_dir * pi / 2 * progress
            y = self.y - 20 * progress + 10 * sin(pi * progress)
            self.image.clip_composite_draw(self.frame * 100, row, 100, 100,
                                           angle, '', self.x, y, 100, 100)
        else:
            if self.state == 'RUN':
                row -= 200
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
