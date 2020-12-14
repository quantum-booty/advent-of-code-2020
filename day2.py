# 1-3 a: abcde
# 1-3 b: cdefg
# 2-9 c: ccccccccc

from collections import Counter
import csv

valid_count = 0
for row in csv.reader(open('inputs/2.csv')):
    counter = Counter(row[3])
    count = counter[row[2]]
    if int(row[0]) <= count <= int(row[1]):
        valid_count += 1

print(valid_count)

##

valid_count = 0
for row in csv.reader(open('inputs/2.csv')):
    psw = row[3]
    pos1 = psw[int(row[0]) - 1]
    pos2 = psw[int(row[1]) - 1]
    letter = row[2]
    if (pos1 == letter) + (pos2 == letter) == 1:
        valid_count += 1

print(valid_count)
