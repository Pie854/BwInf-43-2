import time
from collections import deque

with open('in\labyrinthe0.txt', 'r') as file: #choose file
    inp = [line.strip() for line in file][::-1]

def input():
    return inp.pop()

num_mazes = 2 #changes the number of mazes (wer hätte es gedacht)
n, m = map(int, input().split())

right = []
down = []
gruben = []

for k in range(num_mazes):
    right.append([[int(j) for j in input().split()] for _ in range(m)])
    down.append([[int(j) for j in input().split()] for _ in range(m - 1)])
    gruben.append([])
    for _ in range(int(input())):
        gruben[k].append(tuple(map(int, input().split())))

t0=time.time()

goal = (m - 1, n - 1)

def compute_areas():
    areas = []
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # R, D, L, U in (dx, dy)
    for k in range(num_mazes):
        cright = right[k]
        cdown = down[k]
        traps = set(gruben[k])
        area = {}
        queue = deque([goal])
        seen = {goal}
        while queue:
            y, x = queue.popleft()
            vals = []
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                # 1) Fallen
                if (nx, ny) in traps:
                    vals.append(-2 * num_mazes)
                # 2) Rand
                elif not (0 <= nx < n and 0 <= ny < m):
                    vals.append(0)
                # 3) Wand
                else:
                    if dx == 1 and cright[y][x] == 1:
                        vals.append(0)
                    elif dx == -1 and cright[y][x - 1] == 1:
                        vals.append(0)
                    elif dy == 1 and cdown[y][x] == 1:
                        vals.append(0)
                    elif dy == -1 and cdown[y - 1][x] == 1:
                        vals.append(0)
                    else:
                        if (ny, nx) in seen:
                            vals.append(1)
                        else:
                            vals.append(-1)
                            seen.add((ny, nx))
                            queue.append((ny, nx))
            area[(y, x)] = vals
        area[goal] = [0, 0, 0, 0]
        areas.append(area)
    return areas

# BFS-Berechnung
areas = compute_areas()

# Absicherung: Start erreichbar?
start = (0, 0)
for k in range(num_mazes):
    if start not in areas[k]:
        print(f"Labyrinth {k} vom Start aus nicht erreichbar!")
        exit()

# Pfadsuche
pos = tuple([start] * num_mazes)
final = tuple([goal] * num_mazes)
seen_states = set()
path = []
steps = 0
moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

while pos != final:
    seen_states.add(pos)
    steps += 1
    best_move = None
    best_score = -float('inf')
    for i, move in enumerate(moves):
        new = []
        score = 0
        valid = True
        for k in range(num_mazes):
            cell_scores = areas[k].get(pos[k], [ -2*num_mazes ] * 4)
            r = cell_scores[i]
            score += r
            if r == -2 * num_mazes:
                valid = False
            if r != 0:
                # Bewegung möglich
                new.append((pos[k][0] + move[1], pos[k][1] + move[0]))
            else:
                new.append(pos[k])
        new_pos = tuple(new)
        if valid and new_pos not in seen_states and score > best_score:
            best_score = score
            best_move = (new_pos, i)

    if best_move is None:
        print('NO SOLUTION FOUND')
        exit()
    pos, mv = best_move
    path.append(mv)

print(len(path))
print(path)
print("Dauer:", time.time() - t0)
