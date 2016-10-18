import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle
from random import *

from kivy.config import Config
Config.set('graphics', 'resizable', 0) #don't make the app re-sizeable
#Graphics fix
 #this fixes drawing issues on some phones
Window.clearcolor = (0, 0, 0, 1.)

class WidgetDrawer(Widget):
    #This widget is used to draw all of the objects on the screen
    #it handles the following:
    # widget movement, size, positioning
    #whenever a WidgetDrawer object is created, an image string need to be
    # specified, example: wid - WidgetDrawer('./image.png')

    # objects of this class must be initiated with an image string
#;You can use **kwargs to let your functions that take an arbitrary number of
# keyword arguments, kwargs ; keyword arguments

    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs)
        with self.canvas:
            self.size = (Window.width*.002*25,
                         Window.width*.002*25)
            self.rect_bg = Rectangle(source = imageStr,
                                     pos = self.pos,
                                     size = self.size)
            self.bind(pos = self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y
            self.pos = (self.x, self.y)
            self.rect_bg.pos = self.pos

    def update_graphics_pos(self, instance, value):
        self.rect_bg.pos = value
    def setSize(self, width, height):
        self.size = (width, height)
    def setPos(xpos, ypos):
        self.x = xpos
        self.y = ypos

class Asteroid(WidgetDrawer):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y
    def update(self):
        self.move()

class Ship(WidgetDrawer):
    impulse = 3
    grav = -0.1

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

        if self.y > Window.height * 0.95:
            self.impulse = -3

    def determineVelocity(self):
        self.grav = self.grav * 1.05

        if self.grav < -4:
            self.grav = -4

        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95 * self.impulse

    def update(self):
        self.determineVelocity()
        self.move()

class MyButton(Button):
    def __init__(self, **kwargs):
        super(MyButton, self).__init_(**kwargs)
        self.font_size = Window.width * 0.018

class GUI(Widget):
    asteroidList = []
    minProb = 1700
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        l = Label(text = 'Flappy Ship')
        l.x = Window.width / 2 - l.width / 2
        l.y = Window.height * 0.8
        self.add_widget(l)

        self.ship = Ship(imageStr = './ship.png')
        self.ship.x = Window.width / 4
        self.ship.y = Window.height / 2
        self.add_widget(self.ship)

    def addAsteroid(self):
        imageNumber = randint(1, 4)
        imageStr = './sandstone_' + str(imageNumber) + '.png'
        tmpAsteroid = Asteroid(imageStr)
        tmpAsteroid.x = Window.width * 0.99

        ypos = randint(1, 16)
        ypos = ypos * Window.height * .0625

        tmpAsteroid.y = ypos
        tmpAsteroid.velocity_y = 0
        vel = 10
        tmpAsteroid.velocity_x = -0.1 * vel

        self.asteroidList.append(tmpAsteroid)
        self.add_widget(tmpAsteroid)

    def on_touch_down(self, touch):
        self.ship.impulse = 3
        self.ship.grav = -0.1

    def GameOver(self):
        restartButton = MyButton(text = 'Restart')

        def restart_button(obj):
            print 'restart button pushed'
            for k in self.asteroidList:
                self.remove_widget(k)

                self.ship.xpos = Window.width * 0.25
                self.ship.ypos = Window.height * 0.25
                self.minProb = 1700
            self.asteroidList = []

            self.parent.remove_widget(restartButton)
            Clock.unschedule(self.update)
            Clock.schedule_interval(self.update, 1.0/60.0)
        restartButton.size = (Window.width*.3, Window.width*.1)
        restartButton.pos = (Window.width*0.5-restartButton.width/2,
                             Window.height)
        restartButton.bind(on_release = restart_button)
        self.parent.add_widget(restartButton)

    def update(self, dt):
        self.ship.update()
        tmpCount = randint(1, 1800)
        if tmpCount > self.minProb:
            self.addAsteroid()
            if self.minProb < 1300:
                self.minProb = 1300
            self.nimProb = self.minProb -1

        for k in self.asteroidList:
            if k.collide_widget(self.ship):
                print 'death'
                self.gameOver()
                Clock.unshcedule(self.update)
            k.update()

class ClientApp(App):

    def build(App):
        parent = Widget()

        app = GUI()
        Clock.schedule_interval(app.update, 1.0/60.0)
        parent.add_widget(app)
        return parent

if __name__ == '__main__' :
    ClientApp().run()
