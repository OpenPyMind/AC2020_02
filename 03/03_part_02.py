from typing import Tuple, List
from functools import reduce


class Terrain:
    def __init__(self, filename: str):
        self.__filename = filename
        self.__terrain_matrix = self.__create_terrain_matrix()
        self.__right_matrix_boundary = len(self.__terrain_matrix[0])
        self.__lower_matrix_boundary = len(self.__terrain_matrix)

    def __create_terrain_matrix(self) -> List[str]:
        with open(self.__filename, "r") as f:
            return [line.rstrip() for line in f.readlines()]

    @property
    def terrain_matrix(self) -> List[str]:
        return self.__terrain_matrix

    @property
    def right_matrix_boundary(self):
        return self.__right_matrix_boundary

    @property
    def lower_matrix_boundary(self):
        return self.__lower_matrix_boundary


class Slope:
    __STARTING_POS = (0, 0)
    __TREE_SYMBOL = "#"
    __INPUT_FILENAME = "input.txt"

    def __init__(self, increments: Tuple[int, int]):
        self.__starting_position = Slope.__STARTING_POS
        self.__y_inc = increments[0]
        self.__x_inc = increments[1]
        self.__tree_symbol = Slope.__TREE_SYMBOL
        self.__terrain = Terrain(Slope.__INPUT_FILENAME)
        self.__tree_count = self.__terrain_matrix_evaluator()

    @property
    def tree_count(self) -> int:
        return self.__tree_count

    def __terrain_matrix_evaluator(self) -> int:
        count = 0
        current_position = self.__starting_position
        while True:
            current_y = current_position[0] + self.__y_inc
            current_x = current_position[1] + self.__x_inc

            if current_y >= self.__terrain.lower_matrix_boundary:
                return count

            if current_x >= self.__terrain.right_matrix_boundary:  # index wrapping
                current_x %= self.__terrain.right_matrix_boundary

            if self.__terrain.terrain_matrix[current_y][current_x] == self.__tree_symbol:
                count += 1

            current_position = (current_y, current_x)


slopes_increments = {
    1: (1, 1),
    2: (1, 3),
    3: (1, 5),
    4: (1, 7),
    5: (2, 1)
}

tree_counts = []
for slope, increments in slopes_increments.items():
    current_slope = Slope(increments)
    tree_counts.append(current_slope.tree_count)

tree_counts_product = reduce(lambda a, b: a * b, tree_counts)
print(tree_counts)
print(tree_counts_product)