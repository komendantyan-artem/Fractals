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

levi_curve = ((Segment(0, 0, 5, -5, -1), Segment(5, -5, 10, 0, -1)),
    [Segment(0, 0, 200, 0, 0)],
    16)

koch_snowflake = ((Segment(0, 0, 10/3, 0, -1), Segment(10/3, 0, 5, sqrt(75)/3, -1),
    Segment(5, sqrt(75)/3, 20/3, 0, -1), Segment(20/3, 0, 10, 0, -1)),
    [Segment(0, 0, 150, 150 * sqrt(3), 0), Segment(150, 150 * sqrt(3), 300, 0, 0),
     Segment(300, 0, 0, 0, 0)], 6)

dragon_curve = ((Segment(5, 0, 0, -5, -1), Segment(5, 0, 10, -5, -1)),
    [Segment(0, 0, 300, 0, 0)],
    16)

curve_like_dragon = ((Segment(5, 0, 0, -5, -1), Segment(5, 0, 10, 5, -1)),
    [Segment(0, 0, 150, 0, 0)],
    16)

sierpinski_triangle = ((Segment(0, 0, 5, 0, -1), Segment(5, 0, 10, 0, -1),
    Segment(5, 0, 2.5, 2.5 * sqrt(3), -1)),
    [Segment(300, 0, 0, 0, 0),
     Segment(0, 0, 150, -150 * sqrt(3), 0), 
     Segment(150, -150 * sqrt(3), 300, 0, 0)], 8)

sierpinski_carpet = ((
    Segment(0   ,    0, 10/3,    0, -1),
    Segment(10/3,    0, 20/3,    0, -1),
    Segment(20/3,    0,   10,    0, -1),
    Segment(10/3,    0, 10/3, 10/3, -1), Segment(10/3, 10/3, 10/3, 0, -1),
    Segment(10/3, 10/3, 10/3, 20/3, -1),
    Segment(20/3,    0, 20/3, 10/3, -1), Segment(20/3, 10/3, 20/3, 0, -1)),
    [Segment(0, 0, 300, 0, 0),
     Segment(300, 0, 300, 300, 0), 
     Segment(300, 300, 0, 300, 0),
     Segment(0, 300, 0, 0, 0)], 4)

triangle_fractal = ((Segment(0, 0, 5, 0, -1), Segment(5, 0, 10, 0, -1),
    Segment(2.5, 2.5 * sqrt(3), 5, 0, -1), Segment(7.5, 2.5 * sqrt(3), 5, 0, -1)),
    [Segment(300, 0, 0, 0, 0),
     Segment(0, 0, 150, -150 * sqrt(3), 0), 
     Segment(150, -150 * sqrt(3), 300, 0, 0)], 4)

new_fractal = ((Segment(0, 0, 7, 0, -1), Segment(3.5, -3.5, 3.5, 3.5, -1)),
    [Segment(0, 0, 500, 0, 0)],
    16)


programm_help = """It's help"""
fractals_examples = """There is fractals"""

#-----------------------#

from tkinter import *

def rendering():
    try:
        tmp = [float(i) for i in text_template.get("0.0", END).split()]
        template = [Segment(tmp[i], tmp[i + 1], tmp[i + 2], tmp[i + 3], -1)
                        for i in range(0, len(tmp), 4)]
    except:
        write_to_helper("Неправильный шаблон.")
        return
    try:
        tmp = [float(i) for i in text_begin.get("0.0", END).split()]
        begin = [Segment(tmp[i], tmp[i + 1], tmp[i + 2], tmp[i + 3], 0)
                        for i in range(0, len(tmp), 4)]
    except:
        write_to_helper("Неправильное начальное состояние.")
        return
    try:
        number_of_generations = int(text_generations.get())
        if number_of_generations < 0:
            write_to_helper("Количество итераций должно быть больше нуля.")
            return
    except:
        write_to_helper("Неправильное количество итераций.")
        return
    
    global _number_of_generations, _segments
    _number_of_generations, _segments = 0, []
    root.after_cancel(ALL)
    rendering2((template, begin, number_of_generations))

def rendering2(fractal, ms=300):
    global _number_of_generations, _segments
    template, begin, number_of_generations = fractal
    if number_of_generations < _number_of_generations:
        return
    canvas.delete(ALL)
    if _segments == []:
        _segments = begin
    else:
        _segments = generate_fractal(template, _segments, _number_of_generations)
    for segment in _segments:
        x1, y1, x2, y2, _ = segment
        x1 += center; x2 += center
        y1 += center; y2 += center
        canvas.create_line(x1, y1, x2, y2)
    _number_of_generations += 1
    root.after(ms, lambda: rendering2(fractal))


def write_to_helper(text):
    text_helper.delete(0.0, END)
    text_helper.insert(1.0, text)
    


center = 400

root = Tk()
root.title("Фракталы")
root.geometry("{0}x{1}".format(center * 2 + 225, center * 2 + 5))
root.resizable(False, False)

canvas = Canvas(root, width = center * 2, height = center * 2, bg="white")
canvas.place(x=0, y=0)

text_template = Text(root, width=25, height=4, wrap=NONE)
text_begin = Text(root, width=25, height=4, wrap=NONE)
text_generations = Entry(root, width=33)
generate_button = Button(root, text="Построить фрактал", width=28, command=rendering)

Label(root, text="Шаблон", width=25).place(x=center*2+10, y=0)
text_template.place(x=center*2+10, y=25)
Label(root, text="Начальное состояние", width=25).place(x=center*2+10, y=100)
text_begin.place(x=center*2+10, y=125)
Label(root, text="Количество итераций", width=25).place(x=center*2+10, y=200)
text_generations.place(x=center*2+10, y=225)
generate_button.place(x=center*2+10, y=250)

text_helper = Text(root, width=25, height=20, wrap=WORD)
button_help = Button(root, text="Помощь", width=28,
    command=lambda: write_to_helper(programm_help))
button_examples = Button(root, text="Примеры", width=28,
    command=lambda: write_to_helper(fractals_examples))

text_helper.place(x=center*2+10, y=400)
button_help.place(x=center*2+10, y=730)
button_examples.place(x=center*2+10, y=760)

root.mainloop()
