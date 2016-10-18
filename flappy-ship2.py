import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.graphics import Rectangle, Color, Canvas
from funtools import partial
from random import *

#setup graphics
from kivy.config import Config
Config.set('graphics', 'resizable', 0)

#Graphics fix
from kivy.core.window import Window;
Window.clearcolor = (0, 0, 0, 1.)
#Window.clearcolor = (1, 0, 0, 1.)

class MyButton(Button):
#class used to get inuform button styles
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.font size = Window.width * 0.018

class SmartMenu(Widget):
#the instance created by this class will appear
#when the game is started for the first time
    buttonList = []

    def __init__(self, **kwargs):
    #create custom events first
        self.register_event_type('on_button_release')

        super(SmartMenu, self).__init__(**kwargs)
        self.layout = BoxLayout(orietation = 'vertical')
        self.layout.width = Window.width/2
        self.layout.height = Window.height/2
        self.layout.x = Window.width/2 - self.layout.width/2
        self.layout.y = Window.height/2 -self.layout.height/2
        self.add_widget(self.layout)

    def on_button_release(self, *args):
        pass

    def callback(self, instance):
        self.buttonText = instance.text
        self.dispatch('on_button_release')

    def addButtons(self):
        for k in self.buttonList:
            tmpBtn = MyButton(text = k)
            tmpBtn.background_color = [.4, .4, .4, .4]
            tmpBtn.bind(on_release = self.callback)
            self.layout.add_widget(tmpBtn)

    def buildUp(self):
        self.addButtons()

class SmartStartMenu(SmartMenu):
    buttonList = ['start', 'about']

    def __init__(self, **kwargs):
        super(SmartStartMenu, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation = 'vertical')
        self.layout.width = Window.width/2
        self.layout.height = Window.height/2
        self.layout.x = Window.width/2 - self.layout.width/2
        self.layout.y = Window.height/2 - self.layout.height/2
        self.add_widget(self.layout)

        self.msg = Label(text = 'Flappy Ship')
        self.msg.font_size = Window.width * 0.07
        self.msg.pos = (Window.width*0.45, Window.height*0.75)
        self.add_widget(self.msg)
        self.img = Image(source = 'lens2.png')
        self.img.size = (Window.width*1.5, Window.height*1.5)
        self.img.pos = (-Window.width*0.2, Window.height*0.2)
        self.img.opacity = 0.35
        self.add_widget(self.img)

class WidgetDrawer(Widget):
    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs)

        with self.canvas:

            self.size = (Window.width*.002*25,Window.width*.002*25)
            self.rect_bg = Rectangle(source= imageStr, pos=self.pos,
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


class ScoreWidget(Widget):
    def __init__(self, **kwargs):
        super(ScoreWidget, self).__init__(**kwargs)
        self.asteroidScore = 0
        self.currentScore = 0
        with self.canvas:
            tmpPos = (Window.width * 0.25, Window.height * 0.25)
            tmpSize = (Window.width * 0.5, Window.height * 0.5)
            Color(0.1, .1, .1)
            self.scoreRect = Rectangle(pos = tmpPos, size = tmpSize)

    def prepare(self):
        try:

            self.finalScore = self.asteroidScore * 100

        except:
            print 'problems getting score'
        self.animateScore()

    def animateScore(self):
        scoreText = 'Score: 0'
        self.scoreLabel = Label(text= scoreText, font_size = '20sp')
        self.scoreLabel.x = Window.width * 0.3
        self.scoreLabel.y = Window.height * 0.3
        self.add_widget(self.scoreLabel)
        Clock.schedule_once(self.updateScore, .1)
        self.drawStars()

    def updateScore(self, dt):
        self.currentScore = self.currentScore + 100
        self.scoreLabel.text = 'Score: ' + str(self.currentScore)
        if self.currentScore &lt; self.finalScore:
            Clock.schedule_once(self.updateScore, 0.1)

    def drawStars(self):
        starNumber = 0
        if self.asteroidScore &gt; 10:
            starNumber = 1
        if self.asteroidScore &gt; 50:
            starNumber = 2
        if self.asteroidScore &gt; 200:
            starNumber = 3
        if self.asteroidScore &gt; 500:
            starNumber = 4
        if self.asteroidScore &gt; 1000:
            starNumber = 5

            with self.canvas:
                starPos = Window.width*0.27, Window.height*0.42
                starSize = Window.width*0.06, Window.width*0.06
                starString = 'gold_star.png'
                if starNumber &lt; 1:
                    starString = 'gray_star.png'
                starRectOne=Rectangle(source=starString,
                                      pos=starPos, size=starSize)
                #rect 2
                starPos = Window.width*0.37, Window.height*0.42
                if starNumber &lt; 2:
                    starString = 'gray_star.png'
                starRectTwo=Rectangle(source=starString,
                                      pos=starPos, size=starSize)
                #rect 3
                starPos = Window.width*0.47, Window.height*0.42
                if starNumber &lt; 3:
                    starString = 'gray_star.png'
                starRectThree=Rectangle(source=starString,
                                      pos=starPos, size=starSize)
                #rect 4
                starPos = Window.width*0.57, Window.height*0.42
                if starNumber &lt; 4:
                    starString = 'gray_star.png'
                starRectFour=Rectangle(source=starString,
                                      pos=starPos, size=starSize)
                #rect 5
                starPos = Window.width*0.67, Window.height*0.42
                if starNumber &lt; 5:
                    starString = 'gray_star.png'
                starRectTwo=Rectangle(source=starString,
                                      pos=starPos, size=starSize)

class Asteroid(WidgetDrawer):
    imageStr = './sandstone_1.png'
    rect_bg = Rectangle(source = imageStr)
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
    flameSize = (Window.width * .03, Window.width * .03)

    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

    #don't let the ship go to far
        if self.y &lt; Window.height*0.05:
            #give upwards impulse
            self.impulse = 1
            self.grav = -0.1

        if self.y &gt; Window.height*0.95:
            self.impulse = -3

    def checkBulletNPCCollision(self, j):
        if self.k.collide_widget(j):
            j.health = j.health - self.k.bulletDamage
            j.attackFLag = 'True'
        #age the bullet
            self.k.age = self.k.lifespan + 10
            
    def checkBulletStageCollision(self, q):
        if self.k.collide_widget(q):
            #if object is asteroid
            try:
                if q.type == 'asteroid':
                    q.health = q.health - self.k.bulletDamage
                    self.k.age = self.k.lifespan + 10
            except:
                print 'couldnt hit asteroid'
                
    def determineVelocity(self):
        self.grav = self.grav * 1.05
        self.grav &lt; -4:
            self.grav = -4
            
        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95 * self.impulse
