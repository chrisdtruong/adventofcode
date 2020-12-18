import pdb
import re
from itertools import takewhile

from input import INPUT

REQUIRED_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    'cid'
]

def check_if_valid_passport_data(passport_data):

    birth_year = int(passport_data['byr'])
    if len(str(birth_year)) != 4 or birth_year < 1920 or birth_year > 2002:
        return False

    issue_year = int(passport_data['iyr'])
    if len(str(issue_year)) != 4 or issue_year < 2010 or issue_year > 2020:
        return False

    exp_year = int(passport_data['eyr'])
    if len(str(exp_year)) != 4 or exp_year < 2020 or exp_year > 2030:
        return False

    height_value = int(''.join(takewhile(str.isdigit, passport_data['hgt'])))
    height_measurement = passport_data['hgt'][len(str(height_value)):]
    if height_measurement == 'cm':
        if height_value < 150 or height_value > 193:
            return False
    elif height_measurement == 'in':
        if height_value < 59 or height_value > 76:
            return False
    else:
        return False

    hair_color = passport_data['hcl']
    if len(hair_color) == 7:
        if not re.search("#[a-f|0-9]{6}", hair_color):
            return False
    else:
        return False

    eye_color = passport_data['ecl']
    if eye_color not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False

    passport_id = passport_data['pid']
    if len(passport_id) != 9:
        return False

    return True


def check_if_valid_passport_fields(passport_data):
    missing_fields = []

    for field in REQUIRED_FIELDS:
        if field not in passport_data:
            missing_fields.append(field)

    if len(missing_fields) == 0:
        return True

    if len(missing_fields) == 1 and 'cid' in missing_fields:
        return True

    return False


def standardize_passport_format(passport_data):
    clean_data = {}

    for line in passport_data.split():
        data = line.split(':')

        clean_data[data[0]] = data[1]
    
    return clean_data


def solve_part_one():
    valid_passports = 0

    batch_of_passports = INPUT.split('\n\n')

    print(f"Passports: {len(batch_of_passports)}")

    for passport in batch_of_passports:
        passport_data = standardize_passport_format(passport)

        if check_if_valid_passport_fields(passport_data) is True:
            valid_passports += 1

    print(valid_passports)


def solve_part_two():
    valid_passports = 0

    batch_of_passports = INPUT.split('\n\n')

    # print(f"Passports: {len(batch_of_passports)}")

    for passport in batch_of_passports:
        passport_data = standardize_passport_format(passport)

        if check_if_valid_passport_fields(passport_data) is True:
            if check_if_valid_passport_data(passport_data) is True:
                valid_passports += 1

    print(valid_passports)



def main():
    # solve_part_one()
    solve_part_two()



if __name__ == '__main__':
    main()