from random import randint

store = []

seen = set()

while len(store) < 8:
    # get the random number between 1 to 10
    x, y = randint(1, 10), randint(1, 10)
    temp = f"{x} {y}"
    if temp not in seen:
        store.append(f"{x} {y}")

pen = ""
for ele in store:
    pen += ele
    pen += "\n"

# set the write file name
filename = "coordinates.txt"
with open(filename, 'w', encoding = "utf-8") as f:
    f.write(pen)