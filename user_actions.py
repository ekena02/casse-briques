from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):
    if self.btn.collide_point(touch.x, touch.y):
        self.object = self.btn
    else:
        self.object = None
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_move(self, touch):
    if self.object:
        self.object.pos[0] = (touch.x - self.object.width / 2)
        if self.object.pos[0] >= self.width - self.object.width:
            self.object.pos[0] = self.width - self.object.width
        if self.object.pos[0] <= 0:
            self.object.pos[0] = 0
        if self.object.pos[1] <= 0:
            self.object.pos[1] = 0
        if self.object.pos[1] >= self.height - self.object.height:
             self.object.pos[1] == self.height - self.object.height

    return super(RelativeLayout, self).on_touch_move(touch)


def on_touch_up(self, touch):
    self.object = None
    return super(RelativeLayout, self).on_touch_up(touch)


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'right':
        self.current_direction = 'right'
        self.current_x = 12

    if keycode[1] == 'left':
        self.current_direction = 'left'
        self.current_x = -12
    if keycode[1]=='enter' and not self.game_over and not self.succes:
        if self.pause == True:
            self.pause=False
            self.succes = False
            self._menuwidget.opacity = 0

        else:
            self.pause=True
            self.succes = False
            self._menuwidget.opacity = 1
        self._text = 'PAUSE'
        self.rgba = self._text_color = (0,1,1,1)
    if self.game_over or self.succes:
        if keycode[1]=='r':
            self.reset_game()



def on_keyboard_up(self, key, window, *args):
    self.current_x = 0
    self.current_direction = None