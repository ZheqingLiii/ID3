# use the random function to get a uniformly distributed random number between 0 and 1
# split dataset into 3 csv files:
# train: ~60%
# test: ~15% - 20%
# validate: ~15% - 20%
import random
import sys

with open(sys.argv[1]) as data:
    with open('train.csv', 'w') as test:
        with open('test.csv', 'w') as train:
            with open('validate.csv', 'w') as validate:
                header = next(data)
                test.write(header)
                train.write(header)
                validate.write(header)
                for line in data:
                    number = random.random()
                    if number <= 0.65:
                        test.write(line)
                    elif number > 0.85:
                        train.write(line)
                    else:
                        validate.write(line)
