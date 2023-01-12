import csv


def contains_number(word):
    for i in range(len(word)):
        if word[i].isdigit() == True:
            return True

    return False


block_list = []
with open('Terms-to-Block.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for x, row in enumerate(reader):
        for y, col in enumerate(row):
            if y == 1:
                block_list.append(row[y])

new_list = []

for i, word in enumerate(block_list):

    if len(block_list[i]) <= 7 and not contains_number(word):
        new_list.append(block_list[i])

print(new_list)
