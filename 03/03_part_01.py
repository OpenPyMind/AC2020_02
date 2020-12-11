with open("input.txt", "r") as f:
    matrix = [line.rstrip() for line in f.readlines()]


inc_y = 1
inc_x = 3
right_boundary = len(matrix[0])
lower_boundary = len(matrix)
tree_symbol = "#"


trees_count = 0

starting_pos = (0, 0)
current_pos = starting_pos
while True:
    current_y, current_x = current_pos[0] + inc_y, current_pos[1] + inc_x
    if current_y >= lower_boundary:
        print(trees_count)
        break
    if current_x >= right_boundary:
        current_x %= right_boundary

    if matrix[current_y][current_x] == tree_symbol:
        trees_count += 1
    current_pos = (current_y, current_x)