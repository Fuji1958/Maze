import turtle

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'
WHITE = "white"

class Maze:
    def __init__(self, mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        mazeFile = open(mazeFileName, 'r')
        rowsInMaze = 0
        for line in mazeFile:
            rowList = []
            col = 0
            for ch in line[:-1]:
                rowList.append(ch)
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)

        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        self.xTranslate = -columnsInMaze / 2
        self.yTranslate = rowsInMaze / 2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.bgcolor(WHITE)  # เปลี่ยนพื้นหลังเป็นสีขาว
        self.wn.setworldcoordinates(-(columnsInMaze - 1) / 2 - .5, -(rowsInMaze - 1) / 2 - .5,
                                    (columnsInMaze - 1) / 2 + .5, (rowsInMaze - 1) / 2 + .5)

    def drawMaze(self):
        self.t.speed(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
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
        for i in range(4):
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

        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)

    def isExit(self, row, col):
        return (row == 0 or
                row == self.rowsInMaze - 1 or
                col == 0 or
                col == self.columnsInMaze - 1)

    def __getitem__(self, idx):
        return self.mazelist[idx]


def searchFrom(maze, startRow, startColumn):
    maze.updatePosition(startRow, startColumn)
    if maze[startRow][startColumn] == OBSTACLE:
        return False

    if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
        return False

    # เช็คเงื่อนไข Exit (เมื่อถึงขอบเขาวงกต)
    if maze.isExit(startRow, startColumn):
        # ล้างหน้าจอ
        maze.t.clear()

        # แสดงข้อความ "Turtle Win" เมื่อเสร็จสิ้นการค้นหา
        maze.t.penup()
        maze.t.goto(0, 0)  # ไปที่ตำแหน่งกลางหน้าจอ
        maze.t.write("Turtle Win", align="center", font=("Arial", 24, "normal"))

        # ซ่อนตัวเต่า
        maze.t.hideturtle()

        # รอให้ผู้ใช้ปิดหน้าต่าง
        turtle.done()
        return True  # พบทางออกแล้ว, หยุดการค้นหา

    maze.updatePosition(startRow, startColumn, TRIED)

    # ใช้การค้นหาในทิศทางต่างๆ
    found = searchFrom(maze, startRow - 1, startColumn) or \
            searchFrom(maze, startRow + 1, startColumn) or \
            searchFrom(maze, startRow, startColumn - 1) or \
            searchFrom(maze, startRow, startColumn + 1)

    if found:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)

    return found


# เริ่มต้นเกมม
myMaze = Maze('maze2.txt')
myMaze.drawMaze()
myMaze.updatePosition(myMaze.startRow, myMaze.startCol)

searchFrom(myMaze, myMaze.startRow, myMaze.startCol)
