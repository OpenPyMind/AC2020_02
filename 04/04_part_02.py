from typing import List
from re import match


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


class TagData:
    def __init__(self, tag_type: str, data: str):
        self.__tag_type = tag_type
        self.__data = data
        self.__is_valid = self.__validate()

    @property
    def is_valid(self):
        return self.__is_valid

    def __validate(self):
        valid_tags = {
            "byr": self.__validate_byr,
            "iyr": self.__validate_iyr,
            "eyr": self.__validate_eyr,
            "hgt": self.__validate_hgt,
            "hcl": self.__validate_hcl,
            "ecl": self.__validate_ecl,
            "pid": self.__validate_pid,
            "cid": self.__validate_pid,
        }
        return valid_tags[self.__tag_type]()

    def __validate_byr(self):
        try:
            data = int(self.__data)
            return data in range(1920, 2003)
        except ValueError:
            return False

    def __validate_iyr(self):
        try:
            data = int(self.__data)
            return data in range(2010, 2021)
        except ValueError:
            return False

    def __validate_eyr(self):
        try:
            data = int(self.__data)
            return data in range(2020, 2031)
        except ValueError:
            return False

    def __validate_hgt(self):
        pattern = r"(^[0-9]{2})(in)$|(^[0-9]{3})(cm)$"
        m = match(pattern, self.__data)
        if not m:
            return False
        mlist = [g for g in m.groups()]
        if "in" in mlist:
            return 59 <= int(m.group(1)) <= 76
        elif "cm" in mlist:
            return 150 <= int(m.group(3)) <= 193

    def __validate_hcl(self):
        pattern = r"^#[0-9a-f]{6}$"
        m = match(pattern, self.__data)
        return True if m else False

    def __validate_ecl(self):
        eye_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        return self.__data in eye_colors

    def __validate_pid(self):
        pattern = r"^[0-9]{9}$"
        m = match(pattern, self.__data)
        return True if m else False

    @staticmethod
    def __validate_cid():
        return True


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
                tag, data = entry.split(":")
                if tag in tags:
                    tag_data_obj = TagData(tag, data)
                    if tag_data_obj.is_valid:
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
