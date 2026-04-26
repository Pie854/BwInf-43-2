from collections import deque
import time

def compress_state(state):
    (pos1,pos2)=state
    i1, j1 = pos1
    i2, j2 = pos2
    index1 = i1 * n + j1
    index2 = i2 * n + j2
    return index1 * total_cells + index2

'''with open('in\labyrinthe0.txt', 'r') as file:
    inp = [line.strip() for line in file][::-1]

def input():
    return(inp.pop())'''

n,m=(int(i) for i in input().split())
total_cells = m * n

right=[]
down=[]
gruben=[set(),set()]

for k in (0,1):
    right.append([[int(j) for j in input().split()] for i in range(m)])
    down.append([[int(j) for j in input().split()] for i in range(m-1)])

    for i in range(int(input())):
        x=[int(j) for j in input().split()]
        gruben[k].add((x[1],x[0]))

t0=time.time()
reach=[]

for k in (0,1):
    reach.append([])
    for i in range(m):
        line=[]
        for j in range(n):
            results=[]
            if j+1<n and not right[k][i][j]:
                if (i,j+1) in gruben[k]:
                    results.append((0,0))
                else:
                    results.append((i,j+1))
            else: results.append((i,j))
            if i+1<m and not down[k][i][j]:
                if (i+1,j) in gruben[k]:
                    results.append((0,0))
                else:
                    results.append((i+1,j))
            else: results.append((i,j))
            if 1<=j and not right[k][i][j-1]:
                if (i,j-1) in gruben[k]:
                    results.append((0,0))
                else:
                    results.append((i,j-1))
            else: results.append((i,j))
            if 1<=i and not down[k][i-1][j]:
                if (i-1,j) in gruben[k]:
                    results.append((0,0))
                else:
                    results.append((i-1,j))
            else: results.append((i,j))
            line.append(results)
        reach[k].append(line)

print(1)
#seen={0}
seen1=((n*m)**2)*[0]
seen1[0]=1
queue = deque([(((0,0), (0,0)),[])])

dist=0

while ((m-1,n-1),(m-1,n-1)) not in queue:
    for _ in range(len(queue)):
        node, path = queue.popleft()
        p0,p1=node
        x=reach[0][p0[0]][p0[1]] if p0!=(m-1,n-1) else [((m-1),(n-1)),((m-1),(n-1)),((m-1),(n-1)),((m-1),(n-1))]
        y=reach[1][p1[0]][p1[1]] if p1!=(m-1,n-1) else [((m-1),(n-1)),((m-1),(n-1)),((m-1),(n-1)),((m-1),(n-1))]
        for i in range(4):
            next_state = (x[i], y[i])
            compressed_state = compress_state(next_state)
            if seen1[compressed_state]==0:
                #seen.add(compressed_state)
                seen1[compressed_state]=1
                queue.append((next_state, path+[i]))
                if next_state==((m-1,n-1),(m-1,n-1)):
                    print(dist+1)
                    print(path)
                    print(time.time()-t0)
                    quit()
    dist+=1
    if not queue:
        print('NO SOLUTION FOUND')
        print(time.time()-t0)
        break