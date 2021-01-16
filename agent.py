import random as rd
import string


class Agent:

    def __init__(self):
        self.value = ""
        self.fitness = 0.
        self.pool = "".join(string.ascii_uppercase) + "".join(string.digits)

    def mutate(self):
        possible = len(self.pool) + 3
        """
        == possible -> remove/add
        == possible - 1 -> switch 2 char
        == possible - 2 -> move 1 char
        """
        choice = rd.randint(0, possible)
        new_value = ""
        if choice == possible:
            list_value = list(self.value)
            if 12 < len(self.value) < 18:
                if rd.randint(0, 1) == 0:
                    list_value \
                        .insert(rd.randint(0, len(list_value) - 1),
                                self.pool[rd.randint(0, len(self.pool) - 1)])
                    self.value = "".join(list_value)
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
                list_value \
                    .insert(rd.randint(0, len(list_value) - 1),
                            self.pool[rd.randint(0, len(self.pool) - 1)])
                self.value = "".join(list_value)

            if new_value != "":
                self.value = new_value

        elif choice == possible - 1:
            pos_1 = rd.randint(0, len(self.value) - 1)
            pos_2 = rd.randint(0, len(self.value) - 1)
            for i in range(len(self.value)):
                if i == pos_1:
                    new_value += self.value[pos_2]
                elif i == pos_2:
                    new_value += self.value[pos_1]
                else:
                    new_value += self.value[i]

            self.value = new_value

        elif choice == possible - 2:
            index = rd.randint(0, len(self.value) - 1)
            char = self.value[index]
            list_value = list(self.value)
            list_value.pop(index)
            list_value \
                .insert(rd.randint(0, len(list_value) - 1), str(char))
            self.value = "".join(list_value)

        else:
            k = rd.randint(0, len(self.value) - 1)
            word = ""
            if k != 0:
                word += self.value[:k]
            word += rd.choice(string.ascii_uppercase + string.digits) + \
                self.value[k + 1:]
            new_value = word
            self.value = new_value

        if not self.is_valid():
            print(self.value)
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
