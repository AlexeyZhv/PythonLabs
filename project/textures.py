import pygame as pg
import numpy as np


COLORS = [
    [0, 0, 0],
    [100, 100, 100],
    [100, 0, 0],
    [0, 100, 0],
    [0, 0, 100], 
    [0, 100, 100], 
    [200, 200, 0]
]

def texdraw(surface, intersection_coord, texture, height, coord, width, shade):
    column = int(intersection_coord / 64 * len(texture[0]))
    for row in range(len(texture)):
        x = coord[0]
        y1 = coord[1] + height * (- 0.5 + row / len(texture))
        y2 = coord[1] + height * (- 0.5 + (row + 1) / len(texture))
        col1 = COLORS[texture[row][column]]
        col = []
        for i in range (len(col1)):
            col.append(int(col1[i] * (1 - shade)))
        pg.draw.line(surface, col, [x, y1], [x, y2], width)
    

texture0 = [[0]]

texture1 = [
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5], 
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5], 
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5], 
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4], 
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4], 
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4], 
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4], 
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5],
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [5, 5, 5, 5, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4]
]

texture2 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 0, 0, 0, 1, 0, 0, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 0, 0, 0, 1, 1, 0, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 1, 1, 1, 1, 1, 1, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 1, 1, 1, 1, 1, 1, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 0, 0, 0, 1, 1, 0, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 0, 0, 0, 1, 0, 0, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

texture3 =  [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 6, 6, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 6, 6, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 4, 4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 4, 4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 6, 6, 6, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 4, 6, 6, 6, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4],
    [4, 6, 6, 6, 6, 6, 6, 4, 4, 4, 6, 6, 6, 6, 4, 4],
    [4, 4, 4, 6, 6, 4, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
]

texture4 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 6, 6, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 6, 6, 4, 4, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 6, 6, 4, 4, 6, 6, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 6, 6, 6, 6, 6, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 4, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 4, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 4, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 4, 4, 4, 4, 6, 6, 4, 4, 4, 4, 4, 5, 5, 5, 5],
    [4, 6, 6, 4, 4, 6, 6, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 6, 6, 6, 6, 6, 6, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 4, 4, 6, 6, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4]
    ]

texture5 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 1, 5, 5, 5, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 5, 5, 5, 5, 5, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 5, 5, 5, 5, 5, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 1, 5, 5, 5, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 1, 1, 1, 4, 4, 1, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 1, 1, 1, 4, 4, 1, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]


TEXTURES = [texture0, texture1, texture2, texture3, texture4, texture5]