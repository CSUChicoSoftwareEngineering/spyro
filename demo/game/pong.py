import spyral
import random
import math

WIDTH = 800
HEIGHT = 600
BG_COLOR = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SIZE = (WIDTH, HEIGHT)
PADDLE_HEIGHT = 150
MAX_SCORE = 7

class Ball(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(20, 20))
        #self.image.draw_circle(BALL_COLOR, (10, 10), 10)
        
        spyral.event.register("pong_score", self._reset)
        spyral.event.register("director.update", self.update)
        self._reset()
        spyral.event.register("form.RadForm.radio1.changed", self.c_red)
        spyral.event.register("form.RadForm.radio2.changed", self.c_white)
        spyral.event.register("form.RadForm.radio3.changed", self.c_blue)
        spyral.event.register("form.MyForm.play.changed", self._reset)
        
    def _reset(self):
        theta = random.random()*2*math.pi
        while ((theta > math.pi/4 and theta < 3*math.pi/4) or
               (theta > 5*math.pi/4 and theta < 7*math.pi/4)):
            theta = random.random()*2*math.pi
        r = 300
        
        self.vel_x = r * math.cos(theta)
        self.vel_y = r * math.sin(theta)
        self.anchor = 'center'
        self.pos = (WIDTH/2, HEIGHT/2)
                
    def update(self, delta):
        self.x += delta * self.vel_x
        self.y += delta * self.vel_y
        
        r = self.rect
        if r.top < 100:
            r.top = 100
            self.vel_y = -self.vel_y
        if r.bottom > HEIGHT:
            r.bottom = HEIGHT
            self.vel_y = -self.vel_y
        
        if r.left < 0:
            spyral.event.handle("pong_score", spyral.Event(side='left'))
            spyral.event.handle("left_score", spyral.Event())
        if r.right > WIDTH:
            spyral.event.handle("pong_score", spyral.Event(side='right'))
            spyral.event.handle("right_score", spyral.Event())
            
    def collide_paddle(self, paddle):
        if self.collide_sprite(paddle):
            self.vel_x = -self.vel_x

    def c_red(self):
        self.image.fill(RED)
    def c_white(self):
        self.image.fill(WHITE)
    def c_blue(self):
        self.image.fill(BLUE)

class Paddle(spyral.Sprite):
    def __init__(self, scene, side):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(20, PADDLE_HEIGHT)).fill(WHITE) 
        if side == 'left':
            self.anchor = 'midleft'
            self.x = 20
        else:
            self.anchor = 'midright'
            self.x = WIDTH - 20
        self.y = HEIGHT/2
        self.side = side
        self.moving = False
        
        up = 'w' if self.side == 'left' else "up"
        down = 's' if self.side == 'left' else "down"
        
        spyral.event.register("input.keyboard.down."+up, self.move_up)
        spyral.event.register("input.keyboard.down."+down, self.move_down)
        spyral.event.register("input.keyboard.up."+up, self.stop_move)
        spyral.event.register("input.keyboard.up."+down, self.stop_move)
        spyral.event.register("director.update", self.update)
        spyral.event.register("pong_score", self._reset)
        
    def move_up(self):
        self.moving = 'up'
    def move_down(self):
        self.moving = 'down'
    def stop_move(self):
        self.moving = False
    def _reset(self):
        self.y = HEIGHT/2
        
    def update(self, delta):
        paddle_velocity = 250
        
        if self.moving == 'up':
            self.y -= paddle_velocity * delta
        elif self.moving == 'down':
            self.y += paddle_velocity * delta
                
        r = self.rect
        if r.top < 0:
            r.top = 0
        if r.bottom > HEIGHT:
            r.bottom = HEIGHT
            
        #self.pos == getattr(r, self.anchor)

class Menu(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(800, 10)).fill(WHITE)
        self.pos = (0, 88)

class MyForm(spyral.Form):
    play = spyral.widgets.ToggleButton("  Play Again")
    l_score = spyral.widgets.Counter("0")
    r_score = spyral.widgets.Counter("0")

class RadForm(spyral.Form):
    radio1 = spyral.widgets.RadioButton()
    radio2 = spyral.widgets.RadioButton()
    radio3 = spyral.widgets.RadioButton()

class Text(spyral.Sprite):
    def __init__(self, scene, text, size, position):
        spyral.Sprite.__init__(self, scene)
        self.font = spyral.Font("./libraries/spyral/resources/fonts/DejaVuSans.ttf", size, (255,255,255))
        self.image = self.font.render(text)
        self.pos = position

class Pong(spyral.Scene):
    def __init__(self, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)
        self.menu = Menu(self)
        self.ball = Ball(self)
        self.left_paddle = Paddle(self, 'left')
        self.right_paddle = Paddle(self, 'right')
        self.form = MyForm(self)
        self.radform = RadForm(self)
        self.left_score = 0
        self.right_score = 0
        self.in_play = True
    
        self.radform.radio1.pos = (100, 30)
        self.radform.radio2.pos = (100, 50)
        self.radform.radio3.pos = (100, 70)


        txt1 = Text(self, "Red", 12, (75, 30))
        txt2 = Text(self, "White", 12, (65, 50))
        txt3 = Text(self, "Blue", 12, (72, 70))

        self.form.l_score.pos = (90, 0)
        self.form.r_score.pos = (690, 0)

        self.win1 = Text(self, "Player 1 Wins!", 24, (315, 150))
        self.win2 = Text(self, "Player 2 Wins!", 24, (315, 150))
        self.win1.visible = False
        self.win2.visible = False
        self.form.play.pos = (355, 50)
        self.form.hide_widget("play")
        
        spyral.event.register("left_score", self._rscore)
        spyral.event.register("right_score", self._lscore)
        spyral.event.register("form.MyForm.play.changed", self.restart)
        spyral.event.register("system.quit", spyral.director.pop)
        spyral.event.register("director.update", self.update)
        spyral.event.register("input.keyboard.down.q", spyral.director.pop)

    def update(self, delta):
        self.ball.collide_paddle(self.left_paddle)
        self.ball.collide_paddle(self.right_paddle)

    def _lscore(self):
        if self.in_play:
            self.left_score = self.left_score + 1
            self.form.l_score.update_text(" " + str(self.left_score))
            if (self.left_score > MAX_SCORE):
                self.form.reveal_widget("play")
                self.win1.visible = True
                self.in_play = False

    def _rscore(self):
        if self.in_play:
            self.right_score = self.right_score + 1
            self.form.r_score.update_text(" " + str(self.right_score))
            if (self.right_score > MAX_SCORE):
                self.form.reveal_widget("play")
                self.win2.visible = True
                self.in_play = False

    def restart(self):
        self.form.hide_widget("play")
        self.left_score = 0
        self.right_score = 0
        self.form.l_score.update_text(" " + str(self.left_score))
        self.form.r_score.update_text(" " + str(self.right_score))
        self.win1.visible = False
        self.win2.visible = False
        self.in_play = True
            


