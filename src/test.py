import random
import multiprocessing.pool as mpool
import metrics
import os
import math

width = 200
height = 16

options = [
    "-",  # an empty space
    "X",  # a solid wall
    "?",  # a question mark block with a coin
    "M",  # a question mark block with a mushroom
    "B",  # a breakable block
    "o",  # a coin
    "|",  # a pipe segment
    "T",  # a pipe top
    "E",  # an enemy
    #"f",  # a flag, do not generate
    #"v",  # a flagpole, do not generate
    #"m"  # mario's start position, do not generate
]

pop_limit = 480

def random_individual():
    g = [random.choices(options, k=width) for row in range(height)]
    g[15][:] = ["X"] * width
    g[14][0] = "m"
    g[7][-1] = "v"
    g[8:14][-1] = ["f"] * 6
    g[14:16][-1] = ["X", "X"]
    return g

def empty_individual():
    g = [["-" for col in range(width)] for row in range(height)]
    g[15][:] = ["X"] * width
    g[14][0] = "m"
    g[7][-1] = "v"
    for col in range(8, 14):
        g[col][-1] = "f"
    for col in range(14, 16):
        g[col][-1] = "X"
    return g

def calculate_fitness(self):
    measurements = metrics.metrics(self.to_level())
    # Print out the possible measurements or look at the implementation of metrics.py for other keys:
    # print(measurements.keys())
    # Default fitness function: Just some arbitrary combination of a few criteria.  Is it good?  Who knows?
    # STUDENT Modify this, and possibly add more metrics.  You can replace this with whatever code you like.
    coefficients = dict(
        meaningfulJumpVariance=0.5,
        negativeSpace=0.6,
        pathPercentage=0.5,
        emptyPercentage=0.6,
        linearity=-0.5,
        solvability=2.0
    )
    self._fitness = sum(map(lambda m: coefficients[m] * measurements[m],
                            coefficients))
    return self
    
batches = os.cpu_count()
if pop_limit % batches != 0:
    print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
batch_size = int(math.ceil(pop_limit / batches))


population = [random_individual() if random.random() < 0.9
                else empty_individual()
                for _g in range(pop_limit)]

pa = random.randint(0, 480 - 1)
print([population[0]])