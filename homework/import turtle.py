import turtle

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'
WHITE = "white"

class Maze:
    def __init__(self, mazeFileName):
        self.mazelist = []
        self.startRow = None
        self.startCol = None

        with open(mazeFileName, 'r') as mazeFile:
            for row_idx, line in enumerate(mazeFile):
                rowList = list(line.strip())
                if 'S' in rowList:
                    self.startRow = row_idx
                    self.startCol = rowList.index('S')
                self.mazelist.append(rowList)

        if self.startRow is None or self.startCol is None:
            raise ValueError("No start position 'S' found in the maze file!")

        self.rowsInMaze = len(self.mazelist)
        self.columnsInMaze = max(len(row) for row in self.mazelist)
        self.xTranslate = -self.columnsInMaze / 2
        self.yTranslate = self.rowsInMaze / 2

        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.bgcolor(WHITE)
        self.wn.setworldcoordinates(-(self.columnsInMaze - 1) / 2 - .5, 
                                    -(self.rowsInMaze - 1) / 2 - .5,
                                    (self.columnsInMaze - 1) / 2 + .5, 
                                    (self.rowsInMaze - 1) / 2 + .5)

    def drawMaze(self):
        self.t.speed(0)
        for y in range(self.rowsInMaze):
            for x in range(len(self.mazelist[y])):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(x + self.xTranslate, -y + self.yTranslate, 'BLACK')
        self.t.color('black')
        self.t.fillcolor('blue')

    def drawCenteredBox(self, x, y, color):
        self.t.up()
        self.t.goto(x - .5, y - .5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x + self.xTranslate, -y + self.yTranslate))
        self.t.goto(x + self.xTranslate, -y + self.yTranslate)

    def dropBreadcrumb(self, color):
        self.t.dot(10, color)

    def updatePosition(self, row, col, val=None):
        if val:
            self.mazelist[row][col] = val
        self.moveTurtle(col, row)

        colors = {
            PART_OF_PATH: 'green',
            OBSTACLE: 'red',
            TRIED: 'black',
            DEAD_END: 'red'
        }
        if val in colors:
            self.dropBreadcrumb(colors[val])

    def isExit(self, row, col):
        return (row == 0 or row == self.rowsInMaze - 1 or
                col == 0 or col == self.columnsInMaze - 1)

    def __getitem__(self, idx):
        return self.mazelist[idx]

def searchFrom(maze, startRow, startColumn):
    maze.updatePosition(startRow, startColumn)

    if maze[startRow][startColumn] in (OBSTACLE, TRIED, DEAD_END):
        return False

    if maze.isExit(startRow, startColumn):
        maze.t.clear()
        maze.t.penup()
        maze.t.goto(0, 0)
        maze.t.write("Turtle Win", align="center", font=("Arial", 24, "normal"))
        maze.t.hideturtle()
        turtle.done()
        turtle.bye()
        return True

    maze.updatePosition(startRow, startColumn, TRIED)

    found = (searchFrom(maze, startRow - 1, startColumn) or
             searchFrom(maze, startRow + 1, startColumn) or
             searchFrom(maze, startRow, startColumn - 1) or
             searchFrom(maze, startRow, startColumn + 1))

    maze.updatePosition(startRow, startColumn, PART_OF_PATH if found else DEAD_END)
    return found

# โหลดและรันเกม
try:
    myMaze = Maze('Maze/homework/maze2.txt')
    myMaze.drawMaze()
    myMaze.updatePosition(myMaze.startRow, myMaze.startCol)
    searchFrom(myMaze, myMaze.startRow, myMaze.startCol)
except FileNotFoundError:
    print("Error: 'maze2.txt' not found. Make sure the file is in the correct directory.")
except ValueError as e:
    print(f"Error: {e}")
    
