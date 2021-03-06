from typing import List


class Passport:
    def __init__(self, data: str):
        self.__data = data
        self.__is_valid = False

    @property
    def data(self):
        return self.__data

    @property
    def is_valid(self):
        return self.__is_valid

    @is_valid.setter
    def is_valid(self, other: bool):
        self.__is_valid = other


class PassportRepository:
    def __init__(self):
        self.__repository: List[Passport] = []

    @property
    def repository(self):
        return self.__repository

    @repository.setter
    def repository(self, passport: Passport):
        self.__repository.append(passport)


class BatchFileReader:
    def __init__(self, filepath: str):
        self.__passport_repository = PassportRepository()
        self.__filepath = filepath

    @property
    def repository(self):
        return self.__passport_repository

    def scan_passports(self):
        with open(self.__filepath, "r") as f:
            current_passport_data = []
            for line in f:
                if line != "\n":
                    current_passport_data.append(line.rstrip())
                else:
                    current_passport_data = " ".join(current_passport_data)
                    current_passport = Passport(current_passport_data)
                    self.__passport_repository.repository.append(current_passport)
                    current_passport_data = []


class PassportRepositoryEvaluator:
    def __init__(self, repository: PassportRepository):
        self.__repository = repository
        self.__valid_passports = []
        self.__invalid_passports = []

    @property
    def all_passports(self):
        return self.valid_passports + self.invalid_passports

    @property
    def valid_passports(self):
        return len(self.__valid_passports)

    @property
    def invalid_passports(self):
        return len(self.__invalid_passports)

    def evaluate_repository(self):
        for passport in self.__repository.repository:
            entry_data = passport.data.split()
            if len(entry_data) < 7:
                continue
            tags = {
                "byr": False,
                "iyr": False,
                "eyr": False,
                "hgt": False,
                "hcl": False,
                "ecl": False,
                "pid": False,
                "cid": False,
            }
            for entry in entry_data:
                tag, _ = entry.split(":")
                if tag in tags:
                    tags[tag] = True

            if all([tags[tag] for tag, value in tags.items()]):
                passport.is_valid = True
            if all([tags[tag] for tag, value in tags.items() if tag != "cid"]) and tags["cid"] is False:
                passport.is_valid = True

    def evaluate_repository_by_passport_validity(self):
        for passport in self.__repository.repository:
            if not passport.is_valid:
                self.__invalid_passports.append(passport)
            else:
                self.__valid_passports.append(passport)


def main():
    batch_file_reader = BatchFileReader("input.txt")
    batch_file_reader.scan_passports()
    passport_repository_evaluator = PassportRepositoryEvaluator(batch_file_reader.repository)
    passport_repository_evaluator.evaluate_repository()
    passport_repository_evaluator.evaluate_repository_by_passport_validity()
    print(passport_repository_evaluator.valid_passports)
    print(passport_repository_evaluator.invalid_passports)
    print(passport_repository_evaluator.all_passports)


if __name__ == "__main__":
    main()
