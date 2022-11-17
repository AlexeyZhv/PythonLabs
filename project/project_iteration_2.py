
import pygame as pg
import numpy as np
from textures import *
import time

width = 1200
height = 800
FOV = 60 
sen = 2
rays_number = 120
fov_rad = FOV * np.pi / 180
scale = width / fov_rad
MODE = "3D"
wall_height = 48
len0 = len(TEXTURES)
colors = ["BLACK", "WHITE", "GREEN", "RED", "RED", "WHITE", "BLUE", "GREEN"]

def new_texture(size):
    a = []
    for i in range(size):
        b = []
        for j in range(size):
            b.append(0)
        a.append(b)
    return a

Level = [                                       #Square only
    [1, 3, 4, 1, 1, 1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 2, 2, 0, 1, 1, 0, 0, 1, 2, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 5, 0, 0, 1, 1, 1, 6, 1, 5, 1, 0, 1, 1],
    [1, 3, 4, 1, 0, 0, 1, 1, 1, 3, 4, 1, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 2, 2, 0, 1, 1, 0, 0, 1, 2, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1]
]

lw = len(Level)
mapscale = (height / (lw * 64))


def rotate(vec, ang):
    return np.dot(vec, [[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])

def move_controls(alpha):
    move = False
    keys = pg.key.get_pressed()
    if keys[pg.K_w] and keys[pg.K_d]:
        alpha += (np.pi / 4)
        move = True
    elif keys[pg.K_d] and keys[pg.K_s]:
        alpha += (3 * np.pi / 4)
        move = True
    elif keys[pg.K_s] and keys[pg.K_a]:
        alpha += (5 * np.pi / 4)
        move = True
    elif keys[pg.K_a] and keys[pg.K_w]:
        alpha += (7 * np.pi / 4)
        move = True
    elif keys[pg.K_w]:
        alpha += (0)
        move = True
    elif keys[pg.K_d]:
        alpha += (np.pi * 0.5)
        move = True
    elif keys[pg.K_s]:
        alpha += (np.pi)
        move = True
    elif keys[pg.K_a]:
        alpha += (np.pi * 1.5)
        move = True
    return alpha, move

def mag(vec): 
    return np.sqrt(np.sum(i**2 for i in vec))
    

class Player:
    def __init__(self, coord, ang, spd, omega):
        self.coord = np.array(coord)
        self.ang = -ang
        self.spd = spd
        self.omega = omega
    def move(self, angle):
        self.coord = self.coord + self.spd / FPS * rotate([1, 0], angle)
    def rotate(self, dirc):
        self.ang += dirc / FPS * self.omega
        if self.ang > 2 * np.pi:
            self.ang -= 2 * np.pi
        elif self.ang < 0:
            self.ang += 2 * np.pi
    def collision(self, i, j, angle):
        shift = rotate([2 * self.spd / FPS, 0], angle)
        return[
            (self.coord[0] <= 64 * (i + 1) + 2 * self.spd / FPS) and (self.coord[0] >= 64 * i - 2 * self.spd / FPS) and (self.coord[1] >= 64 * j - 2 * self.spd / FPS) and (self.coord[1] <= 64 * (j + 1) + 2 * self.spd / FPS),
            (self.coord[0] + shift[0] <= 64 * (i + 1) +  2 * self.spd / FPS) and (self.coord[0] + shift[0] >= 64 * i -  2 * self.spd / FPS) and (self.coord[1] + shift[1] >= 64 * j -  2 * self.spd / FPS) and (self.coord[1] + shift[1] <= 64 * (j + 1) +  2 * self.spd / FPS)
        ]
    def increase_ang(self, value):
        self.ang += value
        if self.ang > 2 * np.pi:
            self.ang -= 2 * np.pi
        elif self.ang < 0:
            self.ang += 2 * np.pi


obs = Player([104, 104], np.pi / 2, 200, 5)

pg.init()
FPS = 60
screen = pg.display.set_mode([width, height])
mapscreen = pg.surface.Surface([height, height])
drawscreen = pg.surface.Surface([height, height])
clock = pg.time.Clock()
finished = False
pg.display.set_caption("RAYCASTER")
font = pg.font.SysFont("comicsansms", 30)
pg.mouse.set_visible(False)
PAUSED = False

while not finished:
    todraw = False
    clock.tick(FPS)
    fps_label = font.render(f"FPS: {int(clock.get_fps())}", True, "RED")

    for event in pg.event.get():                                
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                if MODE == "3D":
                    MODE = "Map"
                else:
                    MODE = "3D"
            if event.key == pg.K_e:
                todraw = True
            if event.key == pg.K_ESCAPE:
                PAUSED = True
    
    #check if there is a wall in front of the player
    i_w = 0
    j_w = 0
    is_wall = False
    if todraw:
        if obs.ang < np.pi / 4 or obs.ang > 7 * np.pi / 4:
            i = int(obs.coord[0] // 64) + 1
            j = int(obs.coord[1] // 64)
            is_wall = Level[j][i]
        elif obs.ang < 3 * np.pi / 4:
            i = int(obs.coord[0] // 64)
            j = int(obs.coord[1] // 64) + 1
            is_wall = Level[j][i]
        elif obs.ang < 5 * np.pi / 4:
            i = int(obs.coord[0] // 64) - 1
            j = int(obs.coord[1] // 64)
            is_wall = Level[j][i]
        elif obs.ang < 7 * np.pi / 4:
            i = int(obs.coord[0] // 64)
            j = int(obs.coord[1] // 64) - 1
            is_wall = Level[j][i]
        k = i
        m = j
    
    #Drawing the wall in editor
    if (is_wall > 0) and todraw and not finished:
        MODE = "Draw"
        tex = TEXTURES[is_wall]
        if is_wall < len0:
            texture = []
            for j in tex:
                row = []
                for i in j:
                    row.append(i)
                texture.append(row)
        else:
            texture = tex
        texscale = height / len(texture)
        COLOR = 0
        while MODE == "Draw":
            chcolor = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        COLOR += 1
                        if COLOR >= len(COLORS):
                            COLOR = 0
                    if event.key == pg.K_e:
                        MODE = "3D"

            left, middle, right = pg.mouse.get_pressed()
            if left:
                chcolor = True
            x, y = pg.mouse.get_pos()

            if chcolor:
                i, j = int(x // texscale), int(y // texscale)
                if i < 0:
                    i = 0
                if j < 0:
                    j = 0
                if i > len(texture) - 1:
                    i = len(texture) - 1
                if j > len(texture) - 1:
                    j = len(texture) - 1
                texture[j][i] = COLOR

            clock.tick(FPS)
            screen.fill("#444444")
            drawscreen.fill("#444444")
            for i in range(len(texture)):
                for j in range(len(texture[0])):
                        pg.draw.rect(drawscreen, COLORS[texture[j][i]], [[texscale * i + 1, texscale * j + 1], [texscale - 2, texscale - 2]])
            pg.draw.circle(drawscreen, "GREY", [x, y], 7)
            pg.draw.circle(drawscreen, COLORS[COLOR], [x, y], 6)
            screen.blit(drawscreen, [(width - height) / 2, 0])
            pg.display.update()
        if is_wall < len0:
            TEXTURES.append(texture)
        Level[m][k] = TEXTURES.index(texture)

    while PAUSED:
        clock.tick(FPS)
        for event in pg.event.get():                                
            if event.type == pg.QUIT:
                finished = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    PAUSED = False
        screen.fill("#444444")
        pg.display.update()
    
    
    pcol = "GREEN"
    alpha, move = move_controls(obs.ang)
    for i in range(lw):
        for j in range(lw):
            if (Level[j][i] > 0) and obs.collision(i, j, alpha)[0]:
                pcol = "YELLOW"
                if obs.collision(i, j, alpha)[1]:
                    move = False
                    pcol = "RED"

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        obs.rotate(1)
    elif keys[pg.K_LEFT]:
        obs.rotate(-1)


    if MODE == "3D":
        obs.increase_ang(sen * pg.mouse.get_rel()[0] / scale)
        pg.mouse.set_pos([width / 2, height / 2])
        

    if move:
        obs.move(alpha)

    if MODE == "3D":
        screen.fill("#444444")
        pg.draw.rect(screen, "#666666", [[0, 0], [width, height / 2]])
    elif MODE == "Map":
        screen.fill("#444444")
        mapscreen.fill("#444444")
        for i in range(lw):
            for j in range(lw):
                if Level[j][i] == 0:
                    pg.draw.rect(mapscreen, colors[0], [[64 * mapscale * i + 1, 64 * mapscale * j + 1], [64 * mapscale - 2, 64 * mapscale - 2]]) 
                else:
                    pg.draw.rect(mapscreen, colors[1], [[64 * mapscale * i + 1, 64 * mapscale * j + 1], [64 * mapscale - 2, 64 * mapscale - 2]])

    #RAYCASTING
    for offset in np.linspace(- fov_rad / 2, fov_rad / 2, rays_number):
        angle = offset + obs.ang
        if angle > 2 * np.pi:
            angle -= 2 * np.pi
        elif angle < 0:
            angle += 2 * np.pi

            #HORIZONTAL
        if (angle > np.pi and angle < 2 * np.pi):             #UP
            j = int(obs.coord[1] // 64 - 1)
            y = 64 * (j + 1)
            x = obs.coord[0] - 1 / np.tan(angle) * (obs.coord[1] - y)
            i = int(x // 64)
            if i in range(lw) and j in range(lw):
                stopped = (Level[j][i] > 0)
                while not stopped:
                    x -= 64 / np.tan(angle)
                    y -= 64
                    i = int(x // 64)
                    j = int(y // 64) - 1
                    if i in range(lw) and j in range(lw):
                        stopped = (Level[j][i] > 0)
                    else:
                        stopped = True
                        y = -1000000
                        x = obs.coord[0] - 1 / np.tan(angle) * (obs.coord[1] - y)
                if i in range(lw) and j in range(lw):
                    hor_cell = [Level[j][i], x % 64]
            else:
                y = -1000000
                x = obs.coord[0] - 1 / np.tan(angle) * (obs.coord[1] - y)

        else:                                                                                          #DOWN
            j = int(obs.coord[1] // 64) + 1
            y = 64 * (j)
            x = obs.coord[0] - 1 / np.tan(angle) * (obs.coord[1] - y)
            i = int(x // 64)
            if i in range(lw) and j in range(lw):
                stopped = (Level[j][i] > 0)
                while not stopped:
                    x += 64 / np.tan(angle)
                    y += 64
                    i = int(x // 64)
                    j = int(y // 64)
                    if i in range(lw) and j in range(lw):
                        stopped = (Level[j][i] > 0)
                    else:
                        stopped = True
                        y = 1000000
                        x = obs.coord[0] - 1 / np.tan(angle) * (obs.coord[1] - y)
                if i in range(lw) and j in range(lw):
                    hor_cell = [Level[j][i], 64 - x % 64]
            else:
                y = 1000000
                x = obs.coord[0] - 1 / np.tan(angle) * (obs.coord[1] - y)

        if not(i in range(lw) and j in range(lw)):
            hor_cell = [0, 0]
        hor_vec = np.array([x, y]) - obs.coord

            #VERTICAL
        if (angle > 0.5 * np.pi and angle < 1.5 * np.pi):             #LEFT
            i = int(obs.coord[0] // 64 - 1)
            x = 64 * (i + 1)
            y = obs.coord[1] + (x - obs.coord[0]) * np.tan(angle)
            j = int(y // 64)
            if i in range(lw) and j in range(lw):
                stopped = (Level[j][i] > 0)
                while not stopped:
                    x -= 64
                    y -= 64 * np.tan(angle)
                    i = int(x // 64 - 1)
                    j = int(y // 64)
                    if i in range(lw) and j in range(lw):
                        stopped = (Level[j][i] > 0)
                    else:
                        stopped = True
                        x = -1000000
                        y = obs.coord[1] + (x - obs.coord[0]) * np.tan(angle)
                if i in range(lw) and j in range(lw):
                    ver_cell = [Level[j][i], 64 - y % 64]
            else:
                x = -1000000
                y = obs.coord[1] + (x - obs.coord[0]) * np.tan(angle)

        else:                                                                                 #RIGHT
            i = int(obs.coord[0] // 64) + 1
            x = 64 * (i)
            y = obs.coord[1] + (x - obs.coord[0]) * np.tan(angle)
            j = int(y // 64)
            if i in range(lw) and j in range(lw):
                stopped = (Level[j][i] > 0)
                while not stopped:
                    x += 64
                    y += 64 * np.tan(angle)
                    i = int(x // 64)
                    j = int(y // 64)
                    if i in range(lw) and j in range(lw):
                        stopped = (Level[j][i] > 0)
                    else:
                        stopped = True
                        x = 1000000
                        y = obs.coord[1] + (x - obs.coord[0]) * np.tan(angle)
                if i in range(lw) and j in range(lw):
                    ver_cell = [Level[j][i], y % 64]
            else:
                x = 1000000
                y = obs.coord[1] + (x - obs.coord[0]) * np.tan(angle)
        if not (i in range(lw) and j in range(lw)):
            ver_cell = [0, 0]
        ver_vec = np.array([x, y]) - obs.coord
    
        #Walls
        if mag(ver_vec) > mag(hor_vec):
            if MODE == "Map":
                pg.draw.line(mapscreen, "#004400", obs.coord * mapscale, (obs.coord + hor_vec) * mapscale)
            elif MODE == "3D":
                texdraw(screen, hor_cell[1], TEXTURES[hor_cell[0]], wall_height / mag(hor_vec) / np.cos(offset) * scale, [(offset + fov_rad / 2) * scale, height / 2], int(width / rays_number) + 1, 0)
        else:
            if MODE == "Map":
                pg.draw.line(mapscreen, "#003300", obs.coord * mapscale, (obs.coord + ver_vec) * mapscale)
            elif MODE == "3D":
                texdraw(screen, ver_cell[1], TEXTURES[ver_cell[0]], wall_height / mag(ver_vec) / np.cos(offset) * scale, [(offset + fov_rad / 2) * scale, height / 2], int(width / rays_number) + 1, 0.5)
    
    if MODE == "Map":
        pg.draw.circle(mapscreen, pcol, obs.coord * mapscale, 5)
        screen.blit(mapscreen, [0.5 * (width - height), 0])

    screen.blit(fps_label, [20, 20])
    pg.display.update()

            

pg.quit()


    
