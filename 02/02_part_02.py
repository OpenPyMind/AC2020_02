from re import findall
from collections import defaultdict

# group 1: lower boundary, group 2: upper boundary, group 3:
pattern = r"([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)"

# dict structure:
#           {
#       n_current_line:
#               {
#           "policy":
#                   {"lower boundary": x, "upper boundary": y, "character": c},
#                   "password": password
#               }
#           }

current_line_n = 0
policy_password = defaultdict(dict)
with open("input.txt", "r") as f:
    f.seek(0)
    for line in f:
        matches = findall(pattern, line.strip())[0]
        policy_password[current_line_n] = defaultdict(dict)
        policy_password[current_line_n]["policy"]["allowed_pos_a"] = (int(matches[0]) - 1)  # - 1 for direct
        policy_password[current_line_n]["policy"]["allowed_pos_b"] = (int(matches[1]) - 1)  # string indexing
        policy_password[current_line_n]["policy"]["character"] = matches[2]
        policy_password[current_line_n]["password"] = matches[3]
        current_line_n += 1

valid_passwords = 0
for policy, data in policy_password.items():
    idx_pos_a = data["policy"]["allowed_pos_a"]
    idx_pos_b = data["policy"]["allowed_pos_b"]
    char_a_in_password = data["password"][idx_pos_a]
    char_b_in_password = data["password"][idx_pos_b]
    policy_character = data["policy"]["character"]

    if policy_character in (char_a_in_password, char_b_in_password):
        if char_a_in_password != char_b_in_password:
            valid_passwords += 1

print(valid_passwords)