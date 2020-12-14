from typing import List


class GroupAnswerRegistry:
    def __init__(self, answers: List[str]):
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
            group_answers = group_answers_raw.strip().split("\n\n")
        return group_answers

    @property
    def answers(self):
        return self.__answers


class GroupAnswerEvaluator:
    def __init__(self):
        self.__filepath = "input.txt"
        self.__group_answer_reader = GroupAnswerReader(self.__filepath)
        self.__group_answer_registry = GroupAnswerRegistry(self.__group_answer_reader.answers)
        self.__evaluated_registry = self.__evaluate_registry()
        self.__sum_of_yes_answers = self.__yes_answer_adder()

    def __evaluate_registry(self):
        group_positive_answers = []
        for group_raw in self.__group_answer_registry.registry:
            group_members_count = group_raw.count("\n") + 1
            group = group_raw.replace("\n", "")
            group_answers_unique = set(group)
            current_group_positive_answers = len([char for char in group_answers_unique
                                                  if group.count(char) == group_members_count])

            group_positive_answers.append(current_group_positive_answers)
        return group_positive_answers

    def __yes_answer_adder(self):
        return sum(self.__evaluated_registry)

    @property
    def sum_of_yes_answers(self):
        return self.__sum_of_yes_answers


def main():
    group_answer_evaluator = GroupAnswerEvaluator()
    print(group_answer_evaluator.sum_of_yes_answers)


if __name__ == "__main__":
    main()