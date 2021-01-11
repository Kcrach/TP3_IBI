import random as rd


class Agent:

    def __init__(self, pool=[]):
        self.value = ""
        self.fitness = 0.
        self.pool = pool

    def mutate(self):
        possible = len(self.pool) + 1
        choice = rd.randint(0, possible)
        new_value = ""
        if choice == possible:
            if 12 < len(self.value) < 18:
                if rd.randint(0, 1) == 0:
                    self.value += self.pool[rd.randint(0, len(self.pool) - 1)]
                else:
                    pos = rd.randint(0, len(self.value) - 1)
                    for i in range(len(self.value)):
                        if i != pos:
                            new_value += self.value[i]
            elif len(self.value) == 18:
                pos = rd.randint(0, len(self.value) - 1)
                for i in range(len(self.value)):
                    if i != pos:
                        new_value += self.value[i]
            else:
                self.value += self.pool[rd.randint(0, len(self.pool) - 1)]

            if new_value != "":
                self.value = new_value

        else:
            pos = rd.randint(0, len(self.value) - 1)
            for i in range(len(self.value)):
                if i == pos:
                    new_value += self.pool[rd.randint(0, len(self.pool) - 1)]
                else:
                    new_value += self.value[i]
            self.value = new_value

        if not self.is_valid():
            print("Error in mutation, invalid length !")

    def is_valid(self):
        return 12 <= len(self.value) <= 18

    def __str__(self):
        return self.value + ": " + str(self.fitness)

    def set_random(self):
        size = rd.randint(12, 18)
        self.value = ""
        for i in range(size):
            self.value += self.pool[rd.randint(0, len(self.pool) - 1)]
