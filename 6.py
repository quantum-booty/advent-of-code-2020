test_input = """abc

a
b
c

ab
ac

a
a
a
a

b"""

with open('inputs/6.txt', 'r') as file:
    input = file.read()


def sum_answers(input, option='union'):
    groups = input.split("\n\n")
    tot_yes = 0
    for group in groups:
        if option == 'union':
            group_yeses = {
                person_yeses
                for line in group.splitlines() for person_yeses in line.strip()
            }
        elif option == 'intersection':
            person_yeses = [set(line) for line in group.splitlines()]
            if person_yeses:
                group_yeses = set.intersection(*person_yeses)
        tot_yes += len(group_yeses)

    return tot_yes


# part1

assert sum_answers(test_input, option='union') == 11
print(sum_answers(input, option='union'))

# part2
assert sum_answers(test_input, option='intersection') == 6
print(sum_answers(input, option='intersection'))
