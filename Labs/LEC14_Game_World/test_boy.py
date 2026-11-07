"""Run with python -m unittest -v; no game window is needed."""
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE

from boy import Boy
from ball import Ball
import game_world


class BallMessageTests(unittest.TestCase):
    def setUp(self):
        for layer in game_world.world:
            layer.clear()
        image_patch = patch.object(Ball, 'image')
        image_patch.start()
        self.addCleanup(image_patch.stop)
        self.addCleanup(lambda: [layer.clear() for layer in game_world.world])
        with patch('boy.load_image'), patch('boy.get_time', return_value=0):
            self.boy = Boy()

    def key(self, key, event_type=SDL_KEYDOWN):
        self.boy.handle_event(SimpleNamespace(type=event_type, key=key))

    def test_idle_and_run_shoot_in_facing_direction_without_changing_state(self):
        for key, direction in ((SDLK_LEFT, '왼쪽'), (SDLK_RIGHT, '오른쪽')):
            self.key(key)
            for state in ('RUN', 'IDLE'):
                if state == 'IDLE':
                    self.key(key, SDL_KEYUP)
                before = (self.boy.state, self.boy.x, self.boy.frame,
                          self.boy.idle_started_at, self.boy.dir)
                with patch('builtins.print') as output:
                    self.key(SDLK_SPACE)
                output.assert_called_once_with(f'{direction}으로 볼을 발사합니다.')
                ball = game_world.world[1][-1]
                self.assertIsInstance(ball, Ball)
                self.assertEqual((ball.x, ball.y, ball.velocity),
                                 (self.boy.x + self.boy.face_dir * 30,
                                  self.boy.y, self.boy.face_dir * 10))
                self.assertEqual(before, (self.boy.state, self.boy.x, self.boy.frame,
                                          self.boy.idle_started_at, self.boy.dir))
                self.assertEqual(self.boy.state, state)

    def test_space_in_sleep_only_wakes_up(self):
        self.boy.fall_asleep()
        with patch('builtins.print') as output:
            self.key(SDLK_SPACE)
        self.assertEqual(self.boy.state, 'IDLE')
        output.assert_not_called()
        self.assertEqual(game_world.world[1], [])

    def test_releasing_space_does_not_shoot_or_wake(self):
        for state in ('IDLE', 'SLEEP'):
            if state == 'SLEEP':
                self.boy.fall_asleep()
            with patch('builtins.print') as output:
                self.key(SDLK_SPACE, SDL_KEYUP)
            output.assert_not_called()
            self.assertEqual(self.boy.state, state)
            self.assertEqual(game_world.world[1], [])

    def test_balls_move_draw_and_are_removed_without_skipping_next_ball(self):
        left = Ball(0, 90, -10)
        right = Ball(800, 90, 10)
        game_world.add_object(left, 1)
        game_world.add_object(right, 1)
        with patch('ball.get_canvas_width', return_value=800):
            game_world.update()
            self.assertEqual((left.x, right.x), (-10, 810))
            self.assertEqual(game_world.world[1], [left, right])
            left.draw()
            Ball.image.draw.assert_called_once_with(-10, 90)
            game_world.update()
        self.assertEqual(game_world.world[1], [])


if __name__ == '__main__':
    unittest.main()
