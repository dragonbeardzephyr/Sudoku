class puzzle:
    def __init__(self, difficulty):
        self.__grid = [[0 for i in range(9)]for j in range(9)]

    def show_grid(self):
        for i in self.__grid:
            for j in i:
                print(j, end = "  ")
            print()

    def generate(self):
        pass

    def validate(self):
        pass

    def solve(self):
        pass


puzzle1 = puzzle()

puzzle1.show_grid()
