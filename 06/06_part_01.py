from typing import List, Set


class GroupAnswerRegistry:
    def __init__(self, answers: List[Set]):
        self.__registry = answers

    @property
    def registry(self):
        return self.__registry


class GroupAnswerReader:
    def __init__(self, filepath: str):
        self.__filepath = filepath
        self.__answers = self.__get_group_answers_from_input()

    def __get_group_answers_from_input(self):
        with open(self.__filepath, "r") as f:
            group_answers_raw = "".join(f.readlines())
            group_answers = [set(answer.replace('\n', '')) for answer in group_answers_raw.split("\n\n")]
        return group_answers

    @property
    def answers(self):
        return self.__answers


class GroupAnswerEvaluator:
    def __init__(self):
        self.__filepath = "input.txt"
        self.__group_answer_reader = GroupAnswerReader(self.__filepath)
        self.__group_answer_registry = GroupAnswerRegistry(self.__group_answer_reader.answers)
        self.__sum_of_yes_answers = self.__yes_answer_adder()

    def __yes_answer_adder(self):
        return sum([len(answer) for answer in self.__group_answer_registry.registry])

    @property
    def sum_of_yes_answers(self):
        return self.__sum_of_yes_answers


def main():
    group_answer_evaluator = GroupAnswerEvaluator()
    print(group_answer_evaluator.sum_of_yes_answers)


if __name__ == "__main__":
    main()