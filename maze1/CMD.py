import time
import os

# เขาวงกตในรูปแบบ List
maze = [
    list("++++++++++++++++++++++++++++++++++++++++++++++"),
    list("+ s             +                            +"),
    list("+  ++++++++++  +++++++++++++  +++++++  ++++  +"),
    list("+           +                 +        +     +"),
    list("+  +++++++  +++++++++++++  +++++++++++++++++++"),
    list("+  +     +  +           +  +                 +"),
    list("+  +  +  +  +  +  ++++  +  +  +++++++++++++  +"),
    list("+  +  +  +  +  +  +     +  +  +  +        +  +"),
    list("+  +  ++++  +  ++++++++++  +  +  ++++  +  +  +"),
    list("+  +     +  +              +           +  +  +"),
    list("+  ++++  +  ++++++++++++++++  +++++++++++++  +"),
    list("+     +  +                    +              +"),
    list("++++  +  ++++++++++++++++++++++  ++++++++++  +"),
    list("+  +  +                    +     +     +  +  +"),
    list("+  +  ++++  +++++++++++++  +  ++++  +  +  +  +"),
    list("+  +  +     +     +     +  +  +     +     +  +"),
    list("+  +  +  +++++++  ++++  +  +  +  ++++++++++  +"),
    list("+                       +  +  +              +"),
    list("++++  +  +  ++++++++++  +  +  +  +++++++++++++"),
    list("+++++++++++++++++++++++e++++++++++++++++++++++"),
]

# หาตำแหน่งของ 's' และ 'e'
start = None
exit_pos = None

for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == "s":
            start = (x, y)
        if maze[y][x] == "e":
            exit_pos = (x, y)

# ทิศทางการเคลื่อนที่ (ขวา, ลง, ซ้าย, ขึ้น) ตามลำดับ
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# ฟังก์ชันเคลียร์หน้าจอ
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# ฟังก์ชันแสดงผลเขาวงกต
def print_maze():
    clear_screen()
    for row in maze:
        print("".join(row))
    time.sleep(0.1)

# ฟังก์ชันให้ 's' เดินทางเดียว (DFS) และแสดง 'D' ที่ทางตัน
def move(x, y, visited):
    if (x, y) == exit_pos:
        print("\n\tEND\t\n")
        return True  # เจอทางออก

    visited.add((x, y))  # จำตำแหน่งที่เดินผ่าน

    possible_moves = 0  # นับจำนวนทางที่เดินได้

    # ลองเดินไปในแต่ละทิศทาง
    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if (nx, ny) not in visited and maze[ny][nx] in (" ", "e"):
            possible_moves += 1  # ถ้ามีทางเดินเพิ่ม

            maze[ny][nx] = "S"  # เดินหน้า
            maze[y][x] = "w"  # ลบตำแหน่งเดิมออก
            print_maze()

            if move(nx, ny, visited):  # ถ้าทางนี้ไปได้เรื่อย ๆ ก็เดินต่อ
                return True

    # ถ้าเดินไม่ได้เลย → แสดง 'D' ที่จุดนี้
    if possible_moves == 0:
        maze[y][x] = "D"
        print_maze()

    return False  # ไม่มีทางไปต่อแล้ว

# เริ่มต้นเคลื่อนที่จาก 's'
move(start[0], start[1], set())
