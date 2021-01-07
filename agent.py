import random as rd


class Agent:

    def __init__(self, pool=[]):
        self.value = ""
        self.fitness = 0.
        self.pool = pool

    def mutate(self):
        pass

    def is_valid(self):
        return 12 <= len(self.value) <= 18

    def __str__(self):
        return self.value + ": " + str(self.fitness)

    def set_random(self):
        size = rd.randint(12, 18)
        self.value = ""
        for i in range(size):
            self.value += self.pool[rd.randint(0, len(self.pool) - 1)]
