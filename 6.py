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
            yeses = {c for line in group.splitlines() for c in line.strip()}
        elif option == 'intersection':
            answers = [set(line) for line in group.splitlines()]
            if answers:
                yeses = set.intersection(*answers)
        tot_yes += len(yeses)

    return tot_yes


# part1

assert sum_answers(test_input, option='union') == 11
print(sum_answers(input, option='union'))

# part2
assert sum_answers(test_input, option='intersection') == 6
print(sum_answers(input, option='intersection'))
