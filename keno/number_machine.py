# coding=utf-8
"""
Draw numbers...fast.
"""
# import ast
import os

try:
    import numpy as np
    HAVE_NUMPY = True
except:
    print("We don't have numpy, simulation will be slower, but startup time might be a bit faster")
    HAVE_NUMPY = False

import random

EIGHTY_NUMBERS = list(range(1, 80))

# DRAWING_COUNT = 0

class StaticNumbersMachine(object):
    """
    When playing against another RPG, any number are good as the next
    including static. Right?
    """
    def __init__(self, spots):
        """
        This maybe could be a Callable or a def.
        :type spots: int
        """
        if spots == 0 or spots > 21:
            raise TypeError("What game is this? {0}".format(spots))
        self.spots = spots


    def draw(self):
        """
        user picks 1 - 10, but lotto draws 20!
        :return:
        """
        # are the boring numbers as good as any other?
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20][0:self.spots]
        return [4, 18, 19, 20, 24, 26, 30, 32, 37, 44, 48, 51, 53, 54, 56, 57, 68, 69, 70, 77][0:self.spots]

class NumbersMachine(object):
    """
    Abstract number drawing machine.
    """
    def __init__(self, spots):
        """
        This maybe could be a Callable or a def.
        :type spots: int
        """
        if spots == 0 or spots > 21:
            raise TypeError("What game is this? {0}".format(spots))
        self.spots = spots


    def draw(self):
        """
        user picks 1 - 10, but lotto draws 20!
        :return:
        """
        # fastest
        global GENERATOR
        global EIGHTY_NUMBERS
        drawing = next(GENERATOR)
        # shave down to numbers we need.
        drawing = drawing[0:self.spots]
        list.sort(drawing)
        return drawing

    def draw_no_caching(self):
        # sample might be faster?
        if not HAVE_NUMPY:
            # slower
            random.shuffle(EIGHTY_NUMBERS)
        else:
            # faster
            np.random.shuffle(EIGHTY_NUMBERS)


        drawing = EIGHTY_NUMBERS[0:self.spots]
        list.sort(drawing)
        return drawing


def pick_twenty():
    global EIGHTY_NUMBERS

    # sample might be faster?
    if not HAVE_NUMPY:
        # slower
        random.shuffle(EIGHTY_NUMBERS)
    else:
        # faster
        np.random.shuffle(EIGHTY_NUMBERS)

    drawing = EIGHTY_NUMBERS[0:20]
    # MUST NOT SORT!!!
    #list.sort(drawing)
    return drawing

def generate_lots_of_numbers():
    file_name = "numbers.txt"
    # search
    if not os.path.isfile(file_name):
        file_name = "../numbers.txt"
    if not os.path.isfile(file_name):
        print("Generating lots of numbers to file")
        with open(file_name, "w+") as file:
            for i in range(0, 100000000):  # 1_000_000):
                file.write(str(pick_twenty())+"\n")
    # else:
    #     with open(file_name, "r") as f:
    #         print("have {0} pre-generated numbers".format(len(f.readlines())))

    with open(file_name, "r") as file:
        for row in file:
            #yield ast.literal_eval(row) # 10.52
            #yield eval(row) # 9.6
            #yield [x for x in map(int,row.replace("[","").replace("]","").split(","))] # 6.86, 6.42, 6.11, 6.29
            yield[x for x in map(int, row[1:len(row)-2].split(","))] # 6.2, 6.05, 6.23, 6.38, 5.74

GENERATOR = generate_lots_of_numbers()

if __name__ == "__main__":
    def run():
        """
        Exercise cod
        :return:
        """
        i = 1
        while i < 5:
            i += 1
            result = next(generate_lots_of_numbers())
            print(result)
        exit()
    def timings():
        """
        Exercise cod
        :return:
        """
        import timeit
        result = timeit.timeit("""import keno.number_machine as k
    i = 1
    while i <100000: 
        i += 1
        next(k.generate_lots_of_numbers())""", number=1)
        print(result)
