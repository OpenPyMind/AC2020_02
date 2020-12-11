from typing import List


def multiplier(data: List[int]):
    def is_2020(a, b):
        return True if a + b == 2020 else False

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if is_2020(data[i], data[j]):
                return data[i] * data[j]


with open("input.txt", "r") as f:
    data = [int(line) for line in f.readlines()]

result = multiplier(data)
print(result)