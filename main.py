import kivy
kivy.require("1.10.1")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.clock import Clock
from functools import partial
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox

from random import randint
import time


Config.set('input','mouse','mouse,multitouch_on_demand')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)


class node:
    def __init__(self,x,y,hori,vert):
        self.x = x
        self.y = y
        self.hori = hori
        self.vert = vert
        self.col = 0


w_width, w_height = 900, 600 - (600 / 10)
width, height = 50, 30
hori, vert = w_width // width, w_height / height
grid = [[node(j * hori, i * vert, hori - 1, vert - 1) for j in range(width)] for i in range(height)]


colour = [1]
colours = [(1,1,1,1),(0,0,0,1)]

interval = [0.1]
wrap = [0]
rules = [2,3,3]


running = [0]
gen = [0]

def paint(x,y,self):
    hori = grid[0][0].hori
    vert = grid[0][0].vert
    gridx = int(x // (hori + 1))
    gridy = int(y // (vert + 1))
    if gridy >= (len(grid)) or gridx >= len(grid[0]) or gridy < 0 or gridx < 0:
        return
    with self.canvas:
        grid[gridy][gridx].col = colour[0]
        Color(*colours[colour[0]])
        Rectangle(pos=(grid[gridy][gridx].x, grid[gridy][gridx].y), size=(hori, vert))
    return


def updateBoard(self):

    with self.canvas:
        Color(.501,.501,.501,1)
        Rectangle(pos=(0,0),size=(900,540))
        for i in grid:
            for j in i:
                Color(*colours[j.col])
                Rectangle(pos=(j.x, j.y), size=(j.hori, j.vert))

    alive = 0

    for i in grid:
        for j in i:
            if j.col:
                alive += 1

    self.parent.atext = str(alive)
    self.parent.gtext = str(gen[0])


def resetCanvas(self):
    self.canvas.clear()
    updateBoard(self)


def simulate(self,*largs):
    if not running[0]:
        return
    N,M = len(grid),len(grid[0])
    grid2 = [[None for x in range(M)] for x in range(N)]
    for i in range(N):
        for j in range(M):
            grid2[i][j] = node(grid[i][j].x,grid[i][j].y,grid[i][j].hori,grid[i][j].vert)
    for i in range(N):
        for j in range(M):
            cnt = 0
            if wrap[0]:
                for k in range(i-1,i+2):
                    for l in range(j-1,j+2):
                        if k==i and l==j:
                            continue
                        cnt += grid[k%N][l%M].col
            else:
                for k in range(max(i-1,0),min(i+2,N)):
                    for l in range(max(j-1,0),min(j+2,M)):
                        if k==i and l==j:
                            continue
                        cnt += grid[k][l].col
            if grid[i][j].col and cnt < rules[0]:
                grid2[i][j].col = 0
            elif grid[i][j].col and cnt <= rules[1]:
                grid2[i][j].col = 1
            elif grid[i][j].col and cnt > rules[1]:
                grid2[i][j].col = 0
            elif not grid[i][j].col and cnt == rules[2]:
                grid2[i][j].col = 1
            else:
                grid2[i][j].col = grid[i][j].col

    for i in range(N):
        for j in range(M):
            grid[i][j] = grid2[i][j]

    gen[0] += 1
    resetCanvas(self)

    Clock.schedule_once(partial(simulate,self),interval[0])



class Touch(Widget):

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self)

    def on_touch_move(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self)


class ToolBar(BoxLayout):

    atext = StringProperty()
    gtext = StringProperty()

    def spinner_clicked(self,value):
        if value=='Live':
            colour[0] = 1
        else:
            colour[0] = 0

    def sim(self):
        running[0] = 1
        gen[0] = 0
        simulate(self.children[0])

    def clear(self):
        running[0] = 0
        gen[0] = 0
        for i in grid:
            for j in i:
                j.col = 0
        resetCanvas(self.children[0])

    def randomize(self):
        running[0] = 0
        gen[0] = 0
        for i in grid:
            for j in i:
                if randint(1,3)==1:
                    j.col = 1
                else:
                    j.col = 0
        resetCanvas(self.children[0])

    def wrap_check(self):
        if wrap[0]:
            wrap[0] = 0
        else:
            wrap[0] = 1


class GameApp(App):
    def build(self):
        self.title = "Conway's Game of Life Simulator"
        tools = ToolBar()
        draw = Touch()
        with draw.canvas:
            Color(.501, .501, .501, 1)
            Rectangle(pos=(0, 0), size=(900, 540))
        with draw.canvas:
            Color(1,1,1,1)
            for i in range(30):
                for j in range(50):
                    Rectangle(pos=(grid[i][j].x, grid[i][j].y), size=(grid[i][j].hori, grid[i][j].vert))
        tools.add_widget(draw)
        return tools


if __name__ == "__main__":
    game = GameApp()
    game.run()