import kivy
kivy.require("1.10.1")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.clock import Clock
from functools import partial
from kivy.config import Config


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


colour = [0]
colours = [(0,0,0,1),(1,1,1,1)]


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


class Touch(Widget):

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self.parent)

    def on_touch_move(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self.parent)


class ToolBar(BoxLayout):
    pass


class GameApp(App):
    def build(self):
        self.title = "Conway's Game of Life Simulator"
        parent = Widget()
        draw = Touch()
        tools = ToolBar()
        parent.add_widget(draw)
        parent.add_widget(tools)
        with parent.canvas:
            Color(.501, .501, .501, 1)
            Rectangle(pos=(0, 0), size=(900, 540))
        with parent.canvas:
            Color(1,1,1,1)
            for i in range(30):
                for j in range(50):
                    Rectangle(pos=(grid[i][j].x, grid[i][j].y), size=(grid[i][j].hori, grid[i][j].vert))
        return parent


if __name__ == "__main__":
    game = GameApp()
    game.run()