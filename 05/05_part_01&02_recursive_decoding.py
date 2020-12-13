from typing import List, Tuple
from itertools import chain


class BoardingPass:
    """ Boarding pass object with binary sequence and concrete seat numbering.
    row: 0 - 127
    col: 0 - 7
    as a tuple"""
    def __init__(self, sequence: str):
        self.__sequence = sequence
        self.__seat: Tuple[int, int] = (0, 0)
        self.__id: int = 0

    @property
    def sequence(self):
        return self.__sequence

    @property
    def seat(self):
        return self.__seat

    @seat.setter
    def seat(self, value: str):
        self.__seat = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value


class PlaneSeatingOrder:
    """Will create a matrix with rows (0 - 127) and columns (0 - 7) filled with False values.
    Values will be set to BoardingPass object if seat is taken, if a seat is taken, ie discovered in the given sequences."""
    def __init__(self):
        self.__seating_matrix = self.__seating_matrix_generator()

    @staticmethod
    def __seating_matrix_generator():
        matrix = [[False for j in range(8)] for i in range(128)]
        return matrix

    @property
    def seating_matrix(self):
        return self.__seating_matrix

    @seating_matrix.setter
    def seating_matrix(self, seat: Tuple[int, int, BoardingPass]):
        row, col, boarding_pass = seat
        self.__seating_matrix[row][col] = boarding_pass


class BoardingPassRegistry:
    """Gets the data list from BoardingPassReader, and stores a Boarding pass object"""

    def __init__(self, boarding_passes: List[str]):
        self.__boarding_passes = boarding_passes
        self.__registry = self.__boarding_pass_data_converter()

    def __boarding_pass_data_converter(self):
        boarding_passes_converted = [BoardingPass(boarding_pass_sequence)
                                     for boarding_pass_sequence
                                     in self.__boarding_passes]
        return boarding_passes_converted

    @property
    def registry(self):
        return self.__registry


class BoardingPassReader:
    """Takes data from input file and stores it as a list"""

    __FILEPATH = "input.txt"

    def __init__(self):
        self.__filepath = BoardingPassReader.__FILEPATH
        self.__boarding_passes = self.__get_boarding_passes_from_file()

    def __get_boarding_passes_from_file(self):
        with open(self.__filepath, "r") as f:
            boarding_passes = [line.rstrip() for line in f.readlines()]
            return boarding_passes

    @property
    def boarding_passes(self):
        return self.__boarding_passes


class BoardingPassEvaluator:
    """Main logic is collected here.
    Boarding pass sequences are decoded.
    Decoded boarding passes are entered into the plane seating order"""
    def __init__(self):
        self.__boarding_pass_reader = BoardingPassReader()
        self.__boarding_pass_registry = BoardingPassRegistry(self.__boarding_pass_reader.boarding_passes)
        self.__plane_seating_order = PlaneSeatingOrder()
        self.__boarding_pass_seat_number_decoder()
        self.__boarding_pass_id_calculator()
        self.__plane_seating_order_updater()
        self.__boarding_pass_highest_id = self.__boarding_pass_highest_id_finder()
        self.__free_seat = self.__free_seat_finder()

    @property
    def free_seat(self):
        return self.__free_seat

    @property
    def boarding_pass_highest_id(self):
        return self.__boarding_pass_highest_id

    def __boarding_pass_seat_number_decoder(self):
        def recursive_position_finder(idx, max_idx, start, end, sequence):
            current_position_range = list(range(start, end))
            if idx > max_idx:
                return current_position_range[0]
            else:
                if sequence[idx] in ("F", "L"):
                    end -= len(current_position_range) // 2
                elif sequence[idx] in ("B", "R"):
                    start += len(current_position_range) // 2
                return recursive_position_finder(idx + 1, max_idx, start, end, sequence)

        for boarding_pass in self.__boarding_pass_registry.registry:
            row = recursive_position_finder(idx=0, max_idx=6, start=0, end=128, sequence=boarding_pass.sequence)
            col = recursive_position_finder(idx=7, max_idx=9, start=0, end=8, sequence=boarding_pass.sequence)

            boarding_pass.seat = (row, col)

    def __boarding_pass_id_calculator(self):
        for boarding_pass in self.__boarding_pass_registry.registry:
            row, col = boarding_pass.seat[0], boarding_pass.seat[1]
            boarding_pass.id = row * 8 + col

    def __plane_seating_order_updater(self):
        for boarding_pass in self.__boarding_pass_registry.registry:
            data = (boarding_pass.seat[0], boarding_pass.seat[1], boarding_pass)
            self.__plane_seating_order.seating_matrix = data

    def __boarding_pass_highest_id_finder(self):
        highest_id = 0
        for boarding_pass in self.__boarding_pass_registry.registry:
            if boarding_pass.id > highest_id:
                highest_id = boarding_pass.id
        return highest_id

    def __free_seat_finder(self):
        flat_list = list(chain(*self.__plane_seating_order.seating_matrix))
        for idx, value in enumerate(flat_list):
            if 0 < idx < len(flat_list) - 1:
                prev_neighbor = flat_list[idx - 1]
                next_neighbor = flat_list[idx + 1]
                if not value and (prev_neighbor and next_neighbor):
                    free_seat_id = prev_neighbor.id + 1
                    return free_seat_id


def main():
    boarding_pass_evaluator = BoardingPassEvaluator()
    print(boarding_pass_evaluator.boarding_pass_highest_id)  # solution to part 1
    print(boarding_pass_evaluator.free_seat)


if __name__ == '__main__':
    main()
