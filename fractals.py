from collections import namedtuple
from math import *

Segment = namedtuple("Segment", "x1 y1 x2 y2 generation")

#Параметры начального отрезка в шаблоне. Начало в (0, 0) Конец в (10, 0)
start_length = 10
start_angle = 0


def get_angle(x1, y1, x2, y2):
    return atan2(y2 - y1, x2 - x1)
    
def get_length(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
def change_segment(segment, x0, y0, rotation, k, generation):
    x1, y1, x2, y2, _ = segment
    length = k * get_length(x1, y1, x2, y2)
    angle = get_angle(x1, y1, x2, y2) + rotation
    
    angle0 = get_angle(0, 0, x1, y1) + rotation
    distance = k * get_length(0, 0, x1, y1)
    x1 = x0 + distance * cos(angle0)
    y1 = y0 + distance * sin(angle0)
    
    x2 = x1 + length * cos(angle)
    y2 = y1 + length * sin(angle)
    return Segment(x1, y1, x2, y2, generation + 1)

def generate_segments(segment, template):
    x1, y1, x2, y2, generation = segment
    x0, y0 = x1 - 0, y1 - 0
    rotation = get_angle(x1, y1, x2, y2) - start_angle
    k = get_length(x1, y1, x2, y2) / start_length
    for i in template:
        yield change_segment(i, x0, y0, rotation, k, generation)

def generate_fractal(template, begin, number_of_generations):
    result = []
    stack = begin[:]
    while stack:
        current_segment = stack.pop()
        if current_segment.generation == number_of_generations:
            result.append(current_segment)
        else:
            for i in generate_segments(current_segment, template):
                stack.append(i)
    return result


#-------Fractals-------#

tree_fractal = ((Segment(0, 0, 10, 0, -1), Segment(10, 0, 15, 5, -1),
    Segment(10, 0, 15, -5, -1)),
    [Segment(0, 0, 0, -100, 0)],
    10)

tree_wind_fractal = ((Segment(0, 0, 10, 0, -1), Segment(10, 0, 14, -6, -1),
    Segment(10, 0, 16, 4, -1)),
    [Segment(0, 0, 0, -100, 0)],
    10)

koch_flake = ((Segment(0, 0, 10/3, 0, -1), Segment(10/3, 0, 5, sqrt(75)/3, -1),
    Segment(5, sqrt(75)/3, 20/3, 0, -1), Segment(20/3, 0, 10, 0, -1)),
    [Segment(0, 0, 150, 150 * sqrt(3), 0), Segment(150, 150 * sqrt(3), 300, 0, 0),
     Segment(300, 0, 0, 0, 0)], 6)

dragon_fractal = ((Segment(5, 0, 0, -5, -1), Segment(5, 0, 10, 5, -1)),
    [Segment(0, 0, 300, 0, 0)],
    16)

#-----------------------#


from tkinter import Tk, Canvas

center = 400
root = Tk()
canvas = Canvas(root, width = center * 2, height = center * 2)
canvas.pack()

fractal = generate_fractal(*dragon_fractal)
for segment in fractal:
    x1, y1, x2, y2 = segment.x1, segment.y1, segment.x2, segment.y2
    x1 += center; x2 += center
    y1 += center; y2 += center
    canvas.create_line(x1, y1, x2, y2)

'''fractal = begin
number_of_generations = 0
def rendering():
    global number_of_generations
    number_of_generations += 1
    fractal = generate_fractal(template, begin, number_of_generations)
    for segment in fractal:
        x1, y1, x2, y2 = segment.x1, segment.y1, segment.x2, segment.y2
        x1 += center; x2 += center
        y1 += center; y2 += center
        canvas.create_line(x1, y1, x2, y2, fill='green')
    root.after(150, rendering)

root.after_idle(rendering)'''
root.mainloop()
