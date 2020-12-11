from typing import List


def multiplier(data: List[int]):
    def is_2020(a, b, c):
        return True if a + b + c == 2020 else False

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            for k in range(j + 1, len(data)):
                if is_2020(data[i], data[j], data[k]):
                    return data[i] * data[j] * data[k]


with open("input.txt", "r") as f:
    data = [int(line) for line in f.readlines()]

result = multiplier(data)
print(result)