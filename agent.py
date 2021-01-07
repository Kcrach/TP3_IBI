

class Agent:

    def __init__(self, pool=[]):
        self.value = ""
        self.fitness = 0.
        self.pool = pool

    def mutate(self):
        pass

    def is_valid(self):
        return 12 <= len(self.value) <= 18
