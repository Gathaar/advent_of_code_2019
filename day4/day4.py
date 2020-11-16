class Validator:
    def __init__(self):
        self.password = ''

    def is_valid(self, password: str) -> bool:
        self.password = password
        dbl = self.has_double()
        increment_only = self.never_decrease()
        return dbl and increment_only

    def has_double(self) -> bool:
        for i in range(len(self.password)-1):
            for j in range(i + 1, len(self.password) - 1):
                if self.password[i] == self.password[j]:
                    return True
        return False

    def never_decrease(self) -> bool:
        for i in range(len(self.password) - 1):
            if int(self.password[i]) > int(self.password[i+1]):
                return False
        return True


def day4(lower_bound: int, upper_bound: int) -> int:
    counter = 0
    v = Validator()
    for i in range(lower_bound, upper_bound + 1):
        if v.is_valid(str(i)):
            counter += 1
            print(f'Password {i} is valid, counter at {counter}')
    return counter


if __name__ == '__main__':
    print(f'Day 4 Part 1 output: {day4(273025, 767253)} valid passwords')
