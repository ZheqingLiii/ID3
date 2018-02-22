# use the random function to get a uniformly distributed random number between 0 and 1
# split dataset into 2 csv files:
# train: 80%
# test: 20%
import random
import sys

with open(sys.argv[1]) as data:
    with open('train.csv', 'w') as test:
        with open('test.csv', 'w') as train:
                header = next(data)
                test.write(header)
                train.write(header)
                for line in data:
                    number = random.random()
                    if number <= 0.80:
                        test.write(line)
                    else:
                        train.write(line)
