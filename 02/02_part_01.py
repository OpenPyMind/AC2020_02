from re import findall
from collections import defaultdict

# group 1: lower boundary, group 2: upper boundary, group 3:
pattern = r"([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)"

# dict structure: {
#       n_current_line:
#           {
#           "policy":
#                   {"lower boundary": x, "upper boundary": y, "character": c},
#                   "password": password
#            }
#       }

current_line_n = 0
policy_password = defaultdict(dict)
with open("input.txt", "r") as f:
    for line in f:
        matches = findall(pattern, line.strip())[0]
        policy_password[current_line_n] = defaultdict(dict)
        policy_password[current_line_n]["policy"]["lower_boundary"] = int(matches[0])
        policy_password[current_line_n]["policy"]["upper_boundary"] = int(matches[1])
        policy_password[current_line_n]["policy"]["character"] = matches[2]
        policy_password[current_line_n]["password"] = matches[3]
        current_line_n += 1

valid_passwords = 0
for policy, data in policy_password.items():
    policy_range = range(data["policy"]["lower_boundary"], data["policy"]["upper_boundary"] + 1)
    policy_character = data["policy"]["character"]
    n_characters_in_password = data["password"].count(policy_character)
    if n_characters_in_password in policy_range:
        valid_passwords += 1

print(valid_passwords)