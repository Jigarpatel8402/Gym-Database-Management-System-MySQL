import random

NUM_ROWS = 2000
MIN_VAL = 10
MAX_VAL = 60


random_column = [random.randint(100,1000) for _ in range(NUM_ROWS)]
random_column1=[random.randint(5, 15) for _ in range(NUM_ROWS)]
# Print each number on a new line
for number in random_column:
    print(number)