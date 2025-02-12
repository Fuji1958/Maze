import time
import os


def load_maze(filename):
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file.readlines()]


maze = load_maze("Maze/homework/maze1.txt")


start = None
exit_pos = None

for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == "s":
            start = (x, y)
        if maze[y][x] == "e":
            exit_pos = (x, y)


if start is None or exit_pos is None:
    print("Error: หา 's' (จุดเริ่มต้น) หรือ 'e' (ทางออก) ไม่เจอ")
    exit()


directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_maze():
    clear_screen()
    for row in maze:
        print("".join(row))
    time.sleep(0.1)


def move(x, y, visited):
    if (x, y) == exit_pos:
        print("\n END \n")
        return True 

    visited.add((x, y)) 

    possible_moves = 0 

    for dx, dy in directions:
        nx, ny = x + dx, y + dy


        if 0 <= ny < len(maze) and 0 <= nx < len(maze[ny]):
            if (nx, ny) not in visited and maze[ny][nx] in (" ", "e"):
                possible_moves += 1  

                maze[ny][nx] = "s"  
                maze[y][x] = "o" 
                print_maze()

                if move(nx, ny, visited): 
                    return True


    if possible_moves == 0:
        maze[y][x] = "D"
        print_maze()

    return False

move(start[0], start[1], set())
