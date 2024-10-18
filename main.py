import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Ellipse, Rectangle, Color, Quad
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, ColorProperty
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
import os
import sys
from kivy.resources import resource_add_path

if hasattr(sys,'_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
else:
    resource_add_path(os.path.dirname(__file__))

class Ping(RelativeLayout):
    from user_actions import on_touch_down, on_touch_up, on_touch_move, on_keyboard_down, on_keyboard_up, \
        keyboard_closed
    x_max = NumericProperty(0)
    y_max = NumericProperty(0)
    ball = None
    vx = 5
    vy = 5
    current_x = 0
    ball_size = 35
    pos_btn_x = 100
    H_SPACING = 1 / 30
    V_SPACING = 1 / 30
    game_over = False
    succes = False
    nb_briques = 10
    briques_coordinates = []
    briques = []
    current_direction = None
    briques_removed = 0
    pause = True
    _menuwidget = ObjectProperty(None)
    _text=StringProperty("Press enter to start\0")
    _text_color = ColorProperty((0,1,1,1))
    text_game_over = 'GAME OVER\n\nPress \'r\'to restart'
    total_text_game_over = ''
    text_succes = 'WIN!!\n\nPress \'r\'to restart'
    text_game_over_index = 0
    text_succes_index = 0
    bool_game_over_fonction = False
    bool_succes_fonction = False
    game_over_own_init = True
    succes_own_init = True


    def __init__(self, **kwargs):
        super(Ping, self).__init__(**kwargs)
        self.btn = Button(text='move me', size_hint=(.20, .03), pos=(self.pos_btn_x, 5))
        self.add_widget(self.btn)
        with self.canvas:
            Color(0,.26,.91,1)
            self.ball = Ellipse(pos=(100, 100), size=(self.ball_size, self.ball_size))

        Clock.schedule_interval(self.update, 1 / 60)
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.init_brique()
        self.get_brique_coordinate()

    def init_brique(self):
        with self.canvas:
            Color(0.8, 0.3, 0.2, 1)
            for i in range(self.nb_briques):
                self.briques.append(Rectangle())

    def get_brique_coordinate(self):
        for i in range(self.nb_briques):
            start_x = 0
            end_x = int((1 / self.H_SPACING) - 2)
            start_y = int((1 / self.V_SPACING) / 2)
            end_y = int((1 / self.V_SPACING) - 2)
            #v_or_h = random.randint(0, 1)  #if 0:vertical else horizontal
            v_or_h = 1
            x = random.randint(start_x, end_x)
            y = random.randint(start_y, end_y)
            while (v_or_h, x, y) in self.briques_coordinates:
                start_x = 0
                end_x = int((1 / self.H_SPACING) - 2)
                start_y = int((1 / self.V_SPACING) / 2)
                end_y = int((1 / self.V_SPACING) - 1)
                v_or_h = random.randint(0, 1)  # if 0:vertical else horizontal
                x = random.randint(start_x, end_x)
                y = random.randint(start_y, end_y)
            self.briques_coordinates.append((v_or_h, x, y))
    def on_size(self,*args):
        self.update_brique()
        self.vy = self.vy*self.height/750
        x = min(self.ball_size * self.height / 750, self.ball_size * self.width / 750)
        self.ball.size = (x,x)
    def reset_game(self):
        for i in range(self.nb_briques):
            self.canvas.remove(self.briques[i])
        self.total_text_game_over = ''
        self.do = False
        self.vx = 5
        self.current_x = 0
        self.ball.pos = (100,100)
        self.game_over = False
        self.text_game_over_index = 0
        self.bool_game_over_fonction = False
        self.succes= False

        self._menuwidget.opacity = 0
        self.debut =True
        self.briques_coordinates = list()
        self.briques = []
        self.current_direction = None
        self.briques_removed = 0
        self.init_brique()
        self.get_brique_coordinate()
        self.btn.pos = (self.pos_btn_x, 5)
        self.pause = True
        self._menuwidget.opacity = 1
        self._text = "Press enter to start\0"

        self._text_color = (0,1,1,1)






    def update_brique(self):
        h_spacing = self.H_SPACING * self.width
        v_spacing = self.V_SPACING * self.height
        for i in range(self.nb_briques):
            briques_coordinate = self.briques_coordinates[i]
            self.remove_brique_if_collided(i)
            v_or_h = briques_coordinate[0]
            x = briques_coordinate[1] * h_spacing
            y = briques_coordinate[2] * v_spacing
            self.briques[i].pos = (x, y)
            if v_or_h == 0:
                self.briques[i].size = (h_spacing, v_spacing * 2)
            else:
                self.briques[i].size = (h_spacing * 2, v_spacing)


        """if self.brique:
            xmin,ymin = self.briques_coordinates[0],self.briques_coordinates[1]
            xmax,ymax = self.briques_coordinates[0]+20,self.briques_coordinates[1]+200
            self.brique.points= [xmin,ymin,xmin,ymax,xmax,ymax,xmax,ymin]
            print("x_min_ball:"+str(self.x_min_ball))
            if self.collide_ball_brique():
                self.canvas.remove(self.brique)
                self.brique = None"""

    def remove_brique_if_collided(self,index):
        ok =False
        ball_size = self.ball_size
        xmin_ball = self.ball.pos[0]
        ymin_ball = self.ball.pos[1]
        xmax_ball = xmin_ball+ball_size
        ymax_ball = ymin_ball+ball_size
        xcenter_ball = (xmin_ball+xmax_ball)/2
        ycenter_ball = (ymin_ball+ymax_ball)/2
        h_spacing = self.H_SPACING * self.width
        v_spacing = self.V_SPACING * self.height
        briques_coordinates = self.briques_coordinates[index]
        v_or_h = briques_coordinates[0]

        xmin_brique = briques_coordinates[1] * h_spacing
        ymin_brique = briques_coordinates[2] * v_spacing
        if v_or_h==0:
            xmax_brique = xmin_brique+h_spacing
            ymax_brique = ymin_brique+v_spacing*2
        else:
            xmax_brique = xmin_brique + h_spacing*2
            ymax_brique = ymin_brique + v_spacing
        if (ymin_ball+self.vy<ymax_brique<ymin_ball-self.vy and self.vy<0  and xmin_brique-ball_size/2<=xcenter_ball<=xmax_brique+ball_size/2)\
                or (ymax_ball-self.vy<ymin_brique<ymax_ball+self.vy and self.vy>0  and xmin_brique-ball_size/2<=xcenter_ball<=xmax_brique+ball_size/2):
            self.briques_coordinates[index] = (0, 100, 0)
            self.vy *= -1
            ok=True

        if (xmax_ball-3<=xmin_brique<=xmax_ball+3 and ymin_brique-ball_size/2<ycenter_ball<ymax_brique+ball_size/2 and self.vx>0)\
                or (xmin_ball-3<=xmax_brique<=xmin_ball+3 and ymin_brique-ball_size/2<ycenter_ball<ymax_brique+ball_size/2 and self.vx<0):
            self.briques_coordinates[index] = (0, 100, 0)
            self.vx *=-1
            if not ok:
                ok=True
        if ok:
            self.briques_removed+=1
            print('brique_removed:' + str(self.briques_removed))


    def rebondir_ball(self):
        rebond = self.btn.pos[1] + self.btn.size[1]
        x, y = self.ball.pos
        sx, sy = self.ball.size
        if x + sx >= self.width:
            x = self.width - sx
            self.vx *= -1
        if x < 0:
            x = 0
            self.vx *= -1
        if y >= self.height - sy:
            y = self.height - sy
            self.vy *= -1
        if y <= rebond and self.btn.pos[0] <= x + sx / 2 <= self.btn.pos[0] + self.btn.size[0]:
            y = rebond
            self.vy *= -1
            if self.current_direction == 'right' and self.vx > 0:
                if abs(self.vx)<7:self.vx += 2
            elif self.current_direction == 'right' and self.vx <= 0:
                self.vx = random.randint(3,7)
            elif self.current_direction == 'left' and self.vx < 0:
                if abs(self.vx)<7:self.vx -= 2
            elif self.current_direction == 'left' and self.vx >= 0:
                self.vx = -random.randint(3,7)
            
        if y < 0:
            print("perdu")
            self.game_over = True
            return False
        y += self.vy
        x += self.vx
        self.ball.pos = (x, y)
        self.x_min_ball = x
        self.x_max_ball = x + self.ball.size[0]
        self.y_min_ball = y
        self.y_max_ball = y + self.ball.size[1]

    def update(self, dt):
        print("vy:"+str(self.vy))
        self.update_brique()
        if not self.pause and not self.game_over and not self.succes:

            self.btn.pos[0] += self.current_x
            if self.btn.pos[0] < 0:
                self.btn.pos[0] = 0
            if self.btn.pos[0] + self.btn.size[0] >= self.width:
                self.btn.pos[0] = self.width - self.btn.size[0]
            if not self.game_over:
                self.rebondir_ball()

            if self.briques_removed == self.nb_briques:
                self.succes = True
                self._menuwidget.opacity = 1
                self._text = ''
                self._text_color = (.1, 1, .3, 1)
                if self.succes_own_init:
                    self.succes_fonction_primitive()
                else:
                    self._text = self.text_succes

            if self.game_over:
                self._menuwidget.opacity =1
                self._text = ''
                self._text_color = (1,.2,0,1)
                text_score = f"\n\nSCORE: {self.briques_removed}"
                self.total_text_game_over = self.text_game_over[:9]+text_score+self.text_game_over[9:]
                if self.game_over_own_init:
                    self.game_over_fonction_primitive()
                else:
                    self._text = self.total_text_game_over
                #self.total_text_game_over = ''

            if self.succes:
                self._menuwidget.opacity = 1
                self._text = ''
                self._text_color = (.1, 1, .3, 1)

                if self.succes_own_init:
                    self.succes_fonction_primitive()
                else:
                    self._text = self.text_succes
                #Clock.schedule_interval(self.game_over_fonction,.051)

    def game_over_fonction_primitive(self):
        Clock.schedule_interval(self.game_over_fonction,0.051)
    def succes_fonction_primitive(self):
        Clock.schedule_interval(self.succes_fonction,0.051)
    def game_over_fonction(self,dt):
        try:
            if not self.bool_game_over_fonction:
                print('game_over_fonction')
                if len(self._text)<len(self.total_text_game_over):
                    #print('self.text_game_over_index:'+str(self.text_game_over_index))
                    i = self.text_game_over_index
                    self._text +=self.total_text_game_over[self.text_game_over_index]
                    self.text_game_over_index +=1

                else:
                    self.bool_game_over_fonction = True
                    self.game_over_own_init = False
        except:pass

    def succes_fonction(self,dt):
        try:
            if not self.bool_succes_fonction:

                if len(self._text)<len(self.text_succes):
                    i = self.text_succes_index
                    self._text +=self.text_succes[i]
                    self.text_succes_index +=1

                else:
                    self.bool_succes_fonction = True
                    self.succes_own_init = False
                    print(f'len(self._text):{len(self._text)}\n len(self.text_game_over):{len(self.text_game_over)}')
        except:
            pass







class CasseBriqueApp(App):
    def build(self):
        return Ping()


if __name__ == '__main__':
    CasseBriqueApp().run()