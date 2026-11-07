from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.velocity = velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        if self.x < -11 or self.x > get_canvas_width() + 11:
            game_world.remove_object(self)
