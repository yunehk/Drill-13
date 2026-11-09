"""Headless behavior checks; run with python test_item_modes.py."""
import importlib
import sys
import types
import unittest
from unittest.mock import Mock


class ItemModeTests(unittest.TestCase):
    def setUp(self):
        self.original_modules = sys.modules.copy()
        pico = types.ModuleType('pico2d')
        keys = ['SDL_QUIT', 'SDL_KEYDOWN', 'SDL_KEYUP', 'SDLK_0', 'SDLK_1',
                'SDLK_2', 'SDLK_i', 'SDLK_p', 'SDLK_ESCAPE', 'SDLK_SPACE',
                'SDLK_LEFT', 'SDLK_RIGHT']
        for number, key in enumerate(keys):
            setattr(pico, key, number)
        for name in ['load_image', 'get_events', 'get_time', 'clear_canvas',
                     'update_canvas', 'get_canvas_width', 'get_canvas_height']:
            setattr(pico, name, Mock())
        pico.get_time.return_value = 10
        pico.get_canvas_width.return_value = 800
        pico.get_canvas_height.return_value = 600
        sys.modules['pico2d'] = pico
        sys.modules['sdl2'] = pico
        transitions = types.ModuleType('transitions')
        transitions.Machine = Mock()
        sys.modules['transitions'] = transitions
        for name in ['ball', 'boy', 'grass', 'play_mode', 'item_mode',
                     'game_framework', 'game_world']:
            sys.modules.pop(name, None)
        self.pico = pico
        self.play = importlib.import_module('play_mode')
        self.menu = importlib.import_module('item_mode')
        self.framework = importlib.import_module('game_framework')
        self.world = importlib.import_module('game_world')
        self.items = importlib.import_module('items')
        self.play.init()
        self.framework.stack = [self.play]
        self.framework.running = True

    def tearDown(self):
        for name in list(sys.modules):
            if name not in self.original_modules:
                del sys.modules[name]
        sys.modules.update(self.original_modules)

    def key(self, key, event_type=None, repeat=0):
        return types.SimpleNamespace(type=self.pico.SDL_KEYDOWN if event_type is None else event_type,
                                     key=key, repeat=repeat)

    def open_menu(self):
        self.pico.get_events.return_value = [self.key(self.pico.SDLK_i)]
        self.play.handle_events()
        self.assertIs(self.framework.stack[-1], self.menu)

    def test_selection_and_firing(self):
        for key, item, filename in [(self.pico.SDLK_1, self.items.SMALL, 'ball21x21.png'),
                                    (self.pico.SDLK_2, self.items.LARGE, 'ball41x41.png'),
                                    (self.pico.SDLK_0, self.items.NONE, None)]:
            self.open_menu()
            self.pico.get_events.return_value = [self.key(key)]
            self.menu.handle_events()
            self.assertIs(self.framework.stack[-1], self.play)
            self.assertEqual(self.play.boy.selected_item, item)
            self.world.clear()
            self.pico.load_image.reset_mock()
            self.play.boy.state = 'IDLE'
            self.play.boy.handle_event(self.key(self.pico.SDLK_SPACE))
            balls = self.world.world[1]
            self.assertEqual(len(balls), int(filename is not None))
            if filename:
                self.pico.load_image.assert_called_once_with(filename)
                self.assertEqual(balls[0].velocity, 10)

    def test_frozen_world_timer_and_cancel(self):
        self.open_menu()
        update = self.world.update
        self.world.update = Mock()
        self.menu.update()
        self.world.update.assert_not_called()
        self.world.update = update
        self.play.boy.idle_started_at = 5
        self.pico.get_time.return_value = 30
        self.pico.get_events.return_value = [self.key(self.pico.SDLK_ESCAPE)]
        self.menu.handle_events()
        self.assertEqual(self.play.boy.idle_started_at, 25)
        self.assertEqual(self.play.boy.selected_item, self.items.SMALL)

    def test_key_release_and_repeat(self):
        self.open_menu()
        self.play.boy.handle_event = Mock()
        release = self.key(self.pico.SDLK_LEFT, self.pico.SDL_KEYUP)
        self.pico.get_events.return_value = [release]
        self.menu.handle_events()
        self.play.boy.handle_event.assert_called_once_with(release)
        self.pico.get_events.return_value = [self.key(self.pico.SDLK_i, repeat=1)]
        self.menu.handle_events()
        self.assertIs(self.framework.stack[-1], self.menu)
        self.pico.get_events.return_value = [self.key(self.pico.SDLK_i)]
        self.menu.handle_events()
        self.assertIs(self.framework.stack[-1], self.play)

    def test_window_close(self):
        self.open_menu()
        self.pico.get_events.return_value = [self.key(0, self.pico.SDL_QUIT)]
        self.menu.handle_events()
        self.assertFalse(self.framework.running)


if __name__ == '__main__':
    unittest.main()
