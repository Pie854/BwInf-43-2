import heapq
import time
from collections import deque

with open('in\labyrinthe0.txt', 'r') as file: # choose an input
     inp = [line.strip() for line in file][::-1]

def input():
    return(inp.pop())

num_mazes=2 #changes the number of mazes (wer hätte es gedacht)

n,m=(int(i) for i in input().split())
total_cells = m * n

right=[]
down=[]
gruben=[]

for l in range(num_mazes):
    right.append([[int(j) for j in input().split()] for i in range(m)])
    down.append([[int(j) for j in input().split()] for i in range(m-1)])
    gruben.append(set())

    for i in range(int(input())):
        x=[int(j) for j in input().split()]
        gruben[l].add((x[1],x[0]))

t0=time.time()
reach=[]
goal=(m-1,n-1)

for l in range(num_mazes):
    reach.append(dict())
    for i in range(m):
        for j in range(n):
            results=[]
            if j+1<n and not right[l][i][j]:
                if (i,j+1) in gruben[l]:
                    results.append((0,0))
                else:
                    results.append((i,j+1))
            else: results.append((i,j))
            if i+1<m and not down[l][i][j]:
                if (i+1,j) in gruben[l]:
                    results.append((0,0))
                else:
                    results.append((i+1,j))
            else: results.append((i,j))
            if 1<=j and not right[l][i][j-1]:
                if (i,j-1) in gruben[l]:
                    results.append((0,0))
                else:
                    results.append((i,j-1))
            else: results.append((i,j))
            if 1<=i and not down[l][i-1][j]:
                if (i-1,j) in gruben[l]:
                    results.append((0,0))
                else:
                    results.append((i-1,j))
            else: results.append((i,j))
            reach[l][(i,j)]=results
    reach[l][goal]=[goal,goal,goal,goal]

dist=[] #contains the distance from the goal for each position in the grid
goal=(m-1,n-1)

for l in range(num_mazes):
    cright=right[l]
    cdown=down[l]
    cd=dict()

    queue=deque([goal])
    seen={goal}

    d=0

    while queue:
        for _ in range(len(queue)):
            pos=queue.popleft()
            a=[]
            y,x=pos

            if not (y==m-1 or cdown[y][x] or (y+1,x) in seen):
                queue.append((y+1,x))
                seen.add((y+1,x))

            if not (x==n-1 or cright[y][x] or (y,x+1) in seen):
                queue.append((y,x+1))
                seen.add((y,x+1))

            if not(y==0 or cdown[y-1][x] or (y-1,x) in seen):
                queue.append((y-1,x))
                seen.add((y-1,x))
            
            if not(x==0 or cright[y][x-1] or (y,x-1) in seen):
                queue.append((y,x-1))
                seen.add((y,x-1))
            
            cd[pos]=d
        d+=1
    dist.append(cd)


start=num_mazes*((0,0),)

open_list=[]
seen={start}

heapq.heappush(open_list,(max(dist[j][start[j]] for j in range(num_mazes)),0,start,[]))
dmin=float('inf')

while open_list:
    s,g,pos, path = heapq.heappop(open_list)
    if s==g:
        break
    g+=1
    for i in range(4):
        npos=[]
        for l in range(num_mazes):
            npos.append(reach[l][pos[l]][i])
        npos=tuple(npos)
        if not npos in seen:
            f=max(dist[j][npos[j]] for j in range(num_mazes))
            heapq.heappush(open_list,(f+g,g,npos,path+[i]))
            seen.add(npos)

if s==g:
    print(g)
    print(path)
else:
    print('NO SOLUTION FOUND')

print(time.time()-t0)

