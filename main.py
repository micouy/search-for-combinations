from dataclasses import dataclass
from enum import Enum
import random
from itertools import combinations
import os
import time


GAME_TIME_S = 120

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
GRAY = '\033[90m'
RESET = '\033[0m'

FULL_SQUARE = "■"
FULL_TRIANGLE = "▲"
FULL_CIRCLE = "●"

HALF_CIRCLE = "◐"
HALF_SQUARE = "◧"
HALF_TRIANGLE = "◭"

EMPTY_CIRCLE = "○"
EMPTY_SQUARE = "□"
EMPTY_TRIANGLE = "△"

KEYS = [
    'u', 'i', 'o',
    'j', 'k', 'l',
    'm', ',', '.',
]


class Shape(Enum):
    square = "square"
    triangle = "triangle"
    circle = "circle"


class Color(Enum):
    red = "red"
    green = "green"
    blue = "blue"


class Fill(Enum):
    full = "full"
    half = "half"
    empty = "empty"


SHAPE_FILL_MAPPING = {
    (Shape.triangle, Fill.full): FULL_TRIANGLE,
    (Shape.triangle, Fill.half): HALF_TRIANGLE,
    (Shape.triangle, Fill.empty): EMPTY_TRIANGLE,

    (Shape.circle, Fill.full): FULL_CIRCLE,
    (Shape.circle, Fill.half): HALF_CIRCLE,
    (Shape.circle, Fill.empty): EMPTY_CIRCLE,

    (Shape.square, Fill.full): FULL_SQUARE,
    (Shape.square, Fill.half): HALF_SQUARE,
    (Shape.square, Fill.empty): EMPTY_SQUARE,
}

COLOR_MAPPING = {
    Color.red: RED,
    Color.green: GREEN,
    Color.blue: BLUE,
}


@dataclass(frozen=True, eq=True)
class Cell:
    shape: Shape
    color: Color
    fill: Fill


CHOICES = [
    Cell(shape, color, fill)
    for shape in list(Shape)
    for color in list(Color)
    for fill in list(Fill)
]

ALL_COMBINATIONS = [
    (i, j, k)
    for i in range(9)
    for j in range(9)
    for k in range(9)
    if i < j < k
]


def is_combination_valid(a, b, c):
    n_shapes = len(set([a.shape, b.shape, c.shape]))
    n_fills = len(set([a.fill, b.fill, c.fill]))
    n_colors = len(set([a.color, b.color, c.color]))

    return (
        n_shapes in [1, 3]
        and n_fills in [1, 3]
        and n_colors in [1, 3]
    )


def get_combination_cells(grid, indices):
    return [grid[index] for index in indices]


def format_cell(cell):
    color = COLOR_MAPPING[cell.color]
    shape_fill = SHAPE_FILL_MAPPING[(cell.shape, cell.fill)]

    return format_in_color(shape_fill, color)


def format_in_color(text, color):
    return f"{color}{text}{RESET}"


def print_grid(grid):
    for i, (key, cell) in enumerate(zip(KEYS, grid)):
        f_key = format_in_color(key, GRAY)
        f_cell = format_cell(cell)

        print(f"{f_key}{f_cell}", end="")

        if i % 3 == 2:
            print()
        else:
            print(" ", end="")


def get_valid_combinations(grid):
    return [
        combination for combination in ALL_COMBINATIONS
        if is_combination_valid(*get_combination_cells(grid, combination))
    ]


def replace_cells(grid, removed_cells):
    choices_left = set(CHOICES) - set(grid)
    new_cells = random.sample(list(choices_left), 3)

    return [
        choices_left.pop() if cell in removed_cells else cell
        for cell in grid
    ]


def generate_next_grid(grid, removed_cells):
    while True:
        new_grid = replace_cells(grid, removed_cells)
        valid_combinations = get_valid_combinations(grid)

        if valid_combinations:
            return new_grid, valid_combinations


def generate_first_grid():
    while True:
        grid = random.sample(CHOICES, 9)
        valid_combinations = get_valid_combinations(grid)

        if valid_combinations:
            return grid, valid_combinations


def print_screen(n_combinations_found, seconds_left, grid, valid_combinations, message):
    print(f"{RED}Search{RESET} {GREEN}for{RESET} {BLUE}Combinations{RESET}!")
    print()
    print(f"{n_combinations_found} combinations found")
    print(f"{round(seconds_left)//60}:{round(seconds_left)%60:02} left")
    print()
    print_grid(grid)
    print()
    print(f"{len(valid_combinations)} combinations available")
    print()

    if message:
        print(message)
    else:
        print()

    print()


def take_input():
    indices = [KEYS.index(key) for key in input("Combination: ")]

    assert len(indices) == 3 and len(set(indices)) == 3

    return indices


grid, valid_combinations = generate_first_grid()
message = None
start = time.time()
n_combinations_found = 0

while True:
    os.system('clear')

    seconds_left = GAME_TIME_S - (time.time() - start)

    if seconds_left <= 0:
        break

    print_screen(
        n_combinations_found,
        seconds_left,
        grid,
        valid_combinations,
        message,
    )

    try:
        indices = take_input()
    except KeyboardInterrupt:
        break
    except:
        message = "INVALID INPUT!"

        continue

    seconds_left = GAME_TIME_S - (time.time() - start)

    if seconds_left <= 0:
        break

    cells = get_combination_cells(grid, indices)

    if is_combination_valid(*cells):
        message = "OK!"
        n_combinations_found += 1

        grid, valid_combinations = generate_next_grid(grid, cells)
    else:
        message = "WRONG!"

os.system('clear')
print("No time left!")
print(f"{n_combinations_found} combinations found.")