import os
import time
from collections import deque

class pos:
    def __init__(self, y, x):
        self.y = y
        self.x = x

class Maze:
    def __init__(self):
        self.maze = [
            ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", " ", " ", " ", " ", "X", " ", " ", " ", "X", " ", "X", " ", " ", "X"],
            ["X", "X", "X", "X", " ", "X", " ", "X", " ", "X", " ", "X", " ", "X", "X"],
            ["X", " ", " ", "X", " ", "X", " ", "X", " ", " ", " ", "X", " ", " ", "X"],
            ["X", " ", "X", "X", " ", " ", " ", "X", "X", "X", " ", "X", "X", " ", "X"],
            ["X", " ", "X", " ", " ", "X", "X", "X", " ", "X", " ", " ", " ", " ", "X"],
            ["X", " ", " ", " ", "X", " ", " ", " ", " ", " ", "X", "X", "X", " ", "X"],
            ["X", "X", "X", " ", "X", "X", "X", "X", "X", " ", " ", " ", "X", " ", "X"],
            ["X", " ", " ", " ", "X", " ", " ", " ", "X", "X", "X", " ", "X", " ", "X"],
            ["X", " ", "X", " ", " ", " ", "X", " ", " ", " ", "X", " ", "X", " ", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", " ", "X", " ", "X"],
            ["X", " ", " ", " ", " ", " ", " ", " ", " ", " ", "X", " ", "X", " ", "X"],
            ["X", " ", "X", "X", "X", "X", "X", "X", "X", "X", "X", " ", "X", " ", "X"],
            ["X", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]
        ]

        self.ply = pos(1, 1)  # ตำแหน่งเริ่มต้นของ P
        self.end = pos(11, 9)  # ตำแหน่งเป้าหมาย E
        self.maze[self.ply.y][self.ply.x] = "P"
        self.maze[self.end.y][self.end.x] = "E"

    def isInBound(self, y, x):
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def print(self):
        os.system("cls" if os.name == "nt" else "clear")
        for row in self.maze:
            print(" ".join(row))
        time.sleep(0.2)

    def bfs_solve(self):
        # ทิศทาง: บน, ล่าง, ซ้าย, ขวา
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        queue = deque()
        queue.append((self.ply.y, self.ply.x, []))  # (ตำแหน่ง y, ตำแหน่ง x, เส้นทางก่อนหน้า)
        visited = set()
        visited.add((self.ply.y, self.ply.x))

        while queue:
            y, x, path = queue.popleft()

            # ถ้าถึงจุดหมายให้ return เส้นทาง
            if (y, x) == (self.end.y, self.end.x):
                return path

            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if self.isInBound(ny, nx) and (ny, nx) not in visited and self.maze[ny][nx] in [" ", "E"]:
                    queue.append((ny, nx, path + [(ny, nx)]))
                    visited.add((ny, nx))

        return None  # ถ้าไม่มีเส้นทางไปถึง E

    def auto_move(self):
        path = self.bfs_solve()
        if not path:
            print("No path found!")
            return
        
        for y, x in path:
            self.maze[self.ply.y][self.ply.x] = " "
            self.ply.y, self.ply.x = y, x
            self.maze[y][x] = "P"
            self.print()

        self.printEND()

    def printEND(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n>>>>> Congratulations!!! <<<<<\n")

if __name__ == '__main__':
    m = Maze()
    m.print()
    m.auto_move()
