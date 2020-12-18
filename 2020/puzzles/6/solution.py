import pdb
import re
from itertools import takewhile

from input import INPUT


def get_passenger_forms():
    return INPUT.split('\n\n')


def process_passenger_form(form):
    form_rows = form.split('\n')
    form_answer_string = ''.join(form_rows)
    return set([char for char in form_answer_string])


def process_passenger_form_v2(form):
    valid_answers = 0

    form_rows = form.split('\n')

    if len(form_rows) == 1:
        valid_answers = len([ char for char in form_rows[0]])
    else:
        questions = {}
        for form in form_rows:
            for char in form:
                if char not in questions:
                    questions[char] = 0

                questions[char] += 1

        for count in questions.values():
            if len(form_rows) == count:
                valid_answers += 1

    return valid_answers


def solve_part_one():
    forms = get_passenger_forms()

    sum_of_answers = 0
    
    for form in forms:
        answers = process_passenger_form(form)

        sum_of_answers += len(answers)

    print(sum_of_answers)


def solve_part_two():
    forms = get_passenger_forms()

    sum_of_answers = 0

    # print(process_passenger_form_v2(forms[6]))

    for form in forms:
        answers = process_passenger_form_v2(form)

        sum_of_answers += answers

    print(sum_of_answers)


def main():
    # solve_part_one()
    solve_part_two()


if __name__ == '__main__':
    main()