class Grid:
    def __init__(self, input: list[str]):
        weights = input[0].split()
        self.grid = [list(line) for line in input[1:]]
        self.n = len(self.grid)
        self.m = 0
        for i in range(self.n):
            self.m = max(self.m, len(self.grid[i]))
        for i in range(self.n):
            self.grid[i] += ["o"] * (self.m - len(self.grid[i]))
        order = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == "#":
                    break
                self.grid[i][j] = "o"
            for j in range(self.m - 1, -1, -1):
                if self.grid[i][j] == "#":
                    break
                self.grid[i][j] = "o"
        for j in range(self.m):
            for i in range(self.n):
                if self.grid[i][j] == "#":
                    break
                self.grid[i][j] = "o"
            for i in range(self.n - 1, -1, -1):
                if self.grid[i][j] == "#":
                    break
                self.grid[i][j] = "o"
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == "@" or self.grid[i][j] == "+":
                    self.Ares = [i, j]
                    break
        for j in range(self.m):
            for i in range(self.n):
                if (
                    self.grid[i][j] == "$"
                    or self.grid[i][j] == "*"
                    or self.grid[i][j] == "+"
                ):
                    self.grid[i][j] += weights[order]
                    order += 1
        self.step = 0
        self.direction = 0
        self.action = "u"
        self.state = 0
        self.pushedWeight = 0

    def setAlgorithm(self, algorithm: str):
        self.algorithm = algorithm

    def __getitem__(self, index: int):
        return self.grid[index]

    def next(self):
        if self.step == len(self.algorithm):
            return
        self.action = self.algorithm[self.step]
        if self.action == "u":
            if self.grid[self.Ares[0] - 1][self.Ares[1]] == ".":
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[0] -= 1
            self.AresDirection = 0
        elif self.action == "l":
            if self.grid[self.Ares[0]][self.Ares[1] - 1] == ".":
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[1] -= 1
            self.AresDirection = 1
        elif self.action == "d":
            if self.grid[self.Ares[0] + 1][self.Ares[1]] == ".":
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[0] += 1
            self.AresDirection = 2
        elif self.action == "r":
            if self.grid[self.Ares[0]][self.Ares[1] + 1] == ".":
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[1] += 1
            self.AresDirection = 3
        elif self.action == "U":
            if self.grid[self.Ares[0] - 2][self.Ares[1]] == ".":
                self.grid[self.Ares[0] - 2][self.Ares[1]] = (
                    "*" + self.grid[self.Ares[0] - 1][self.Ares[1]][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0] - 1][self.Ares[1]][1:])
            else:
                self.grid[self.Ares[0] - 2][self.Ares[1]] = (
                    "$" + self.grid[self.Ares[0] - 1][self.Ares[1]][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0] - 1][self.Ares[1]][1:])
            if self.grid[self.Ares[0] - 1][self.Ares[1]][0] == "*":
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[0] -= 1
        elif self.action == "L":
            if self.grid[self.Ares[0]][self.Ares[1] - 2] == ".":
                self.grid[self.Ares[0]][self.Ares[1] - 2] = (
                    "*" + self.grid[self.Ares[0]][self.Ares[1] - 1][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0]][self.Ares[1] - 1][1:])
            else:
                self.grid[self.Ares[0]][self.Ares[1] - 2] = (
                    "$" + self.grid[self.Ares[0]][self.Ares[1] - 1][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0]][self.Ares[1] - 1][1:])
            if self.grid[self.Ares[0]][self.Ares[1] - 1][0] == "*":
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[1] -= 1
        elif self.action == "D":
            if self.grid[self.Ares[0] + 2][self.Ares[1]] == ".":
                self.grid[self.Ares[0] + 2][self.Ares[1]] = (
                    "*" + self.grid[self.Ares[0] + 1][self.Ares[1]][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0] + 1][self.Ares[1]][1:])
            else:
                self.grid[self.Ares[0] + 2][self.Ares[1]] = (
                    "$" + self.grid[self.Ares[0] + 1][self.Ares[1]][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0] + 1][self.Ares[1]][1:])
            if self.grid[self.Ares[0] + 1][self.Ares[1]][0] == "*":
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[0] += 1
        elif self.action == "R":
            if self.grid[self.Ares[0]][self.Ares[1] + 2] == ".":
                self.grid[self.Ares[0]][self.Ares[1] + 2] = (
                    "*" + self.grid[self.Ares[0]][self.Ares[1] + 1][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0]][self.Ares[1] + 1][1:])
            else:
                self.grid[self.Ares[0]][self.Ares[1] + 2] = (
                    "$" + self.grid[self.Ares[0]][self.Ares[1] + 1][1:]
                )
                self.pushedWeight += int(self.grid[self.Ares[0]][self.Ares[1] + 1][1:])
            if self.grid[self.Ares[0]][self.Ares[1] + 1][0] == "*":
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "@"
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            self.Ares[1] += 1
        self.step += 1
        if self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 2
        elif self.state == 2:
            self.state = 1

    def back(self):
        if self.step == 0:
            return
        self.action = self.algorithm[self.step - 1]
        if self.action == "u":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            if self.grid[self.Ares[0] + 1][self.Ares[1]] == ".":
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "@"
            self.Ares[0] += 1
        elif self.action == "l":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            if self.grid[self.Ares[0]][self.Ares[1] + 1] == ".":
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "@"
            self.Ares[1] += 1
        elif self.action == "d":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            if self.grid[self.Ares[0] - 1][self.Ares[1]] == ".":
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "@"
            self.Ares[0] -= 1
        elif self.action == "r":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = " "
            if self.grid[self.Ares[0]][self.Ares[1] - 1] == ".":
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "@"
            self.Ares[1] -= 1
        elif self.action == "U":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "*" + self.grid[self.Ares[0] - 1][self.Ares[1]][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0] - 1][self.Ares[1]][1:])
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "$" + self.grid[self.Ares[0] - 1][self.Ares[1]][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0] - 1][self.Ares[1]][1:])
            if self.grid[self.Ares[0] - 1][self.Ares[1]][0] == "*":
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0] - 1][self.Ares[1]] = " "
            if self.grid[self.Ares[0] + 1][self.Ares[1]] == ".":
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "@"
            self.Ares[0] += 1
        elif self.action == "L":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "*" + self.grid[self.Ares[0]][self.Ares[1] - 1][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0]][self.Ares[1] - 1][1:])
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "$" + self.grid[self.Ares[0]][self.Ares[1] - 1][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0]][self.Ares[1] - 1][1:])
            if self.grid[self.Ares[0]][self.Ares[1] - 1][0] == "*":
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1] - 1] = " "
            if self.grid[self.Ares[0]][self.Ares[1] + 1] == ".":
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "@"
            self.Ares[1] += 1
        elif self.action == "D":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "*" + self.grid[self.Ares[0] + 1][self.Ares[1]][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0] + 1][self.Ares[1]][1:])
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "$" + self.grid[self.Ares[0] + 1][self.Ares[1]][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0] + 1][self.Ares[1]][1:])
            if self.grid[self.Ares[0] + 1][self.Ares[1]][0] == "*":
                self.grid[self.Ares[0] + 1][self.Ares[1]] = "."
            else:
                self.grid[self.Ares[0] + 1][self.Ares[1]] = " "
            if self.grid[self.Ares[0] - 1][self.Ares[1]] == ".":
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "+"
            else:
                self.grid[self.Ares[0] - 1][self.Ares[1]] = "@"
            self.Ares[0] -= 1
        elif self.action == "R":
            if self.grid[self.Ares[0]][self.Ares[1]] == "+":
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "*" + self.grid[self.Ares[0]][self.Ares[1] + 1][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0]][self.Ares[1] + 1][1:])
            else:
                self.grid[self.Ares[0]][self.Ares[1]] = (
                    "$" + self.grid[self.Ares[0]][self.Ares[1] + 1][1:]
                )
                self.pushedWeight -= int(self.grid[self.Ares[0]][self.Ares[1] + 1][1:])
            if self.grid[self.Ares[0]][self.Ares[1] + 1][0] == "*":
                self.grid[self.Ares[0]][self.Ares[1] + 1] = "."
            else:
                self.grid[self.Ares[0]][self.Ares[1] + 1] = " "
            if self.grid[self.Ares[0]][self.Ares[1] - 1] == ".":
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "+"
            else:
                self.grid[self.Ares[0]][self.Ares[1] - 1] = "@"
            self.Ares[1] -= 1
        self.step -= 1
        if self.state == 1:
            self.state = 2
        elif self.state == 2:
            self.state = 1
        if self.step == 0:
            self.state = 0

    def restart(self):
        while self.step > 0:
            self.back()
