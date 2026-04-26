import time
import heapq

with open('in\schmuck_bibel_base9.txt','r') as file: #Hier Name des Beispiels einfügen.
    inp = [line.strip() for line in file][::-1]

def input():
    return(inp.pop())

def path_to_cb(path, letters, c):
    r=len(c)
    C=max(c)

    nodes=[]
    for i in range(C):
        nodes.append([])
    cl=-1
    for i in range(r):
        nodes[c[i]+cl].append([i])
    for i in range(len(path)):
        cl+=1
        nodes.append([])
        q=path[i]
        for i in range(q):
            cp=nodes[cl].pop()
            for i in range(r):
                nodes[cl+c[i]].append(cp+[i])
    j=0
    cb=dict()
    for i in range(len(letters)):
        while not nodes[j]:
            j+=1
        cb[letters[i]]=nodes[j].pop()

    return(cb)

def priority(signature,C):
    s=sum(signature)
    p=[]
    for i in range(C+1):
        p.append(s)
        s-=signature[-i-1]
    return(p)

def shift_signature(signature, C):
    return [([signature[0]] + C * [0])[i] + signature[i+1] for i in range(C)] + [0]

def add_to_signature(signature, q, dv, C):
    return [signature[i] + q * dv[i] for i in range(C + 1)]

def reduce_signature(signature, n, C):
    cs = 0
    new_signature = []
    i=0

    while cs<n:
        cs+=signature[i]
        i+=1
    for j in range(i-1):
        new_signature.append(signature[j])
    new_signature.append(signature[i-1]-cs+n)
    for j in range(i,C+1):
        new_signature.append(0)
        
    return new_signature

def main():
    r=int(input())
    c=[int(i) for i in input().split()]
    C = max(c)

    d=C*[0]
    for i in range(r):
        d[c[i]-1]+=1
    d=tuple(d)
    dv = (-1,) + d

    txt=input()
    t0 = time.time()
    p=[]
    chars=[]

    for char in txt:
        if char in chars:
            p[chars.index(char)]+=1
        else:
            chars.append(char)
            p.append(1)
        
    n=len(p)

    chars=[x for _,x in sorted(zip(p,chars))][::-1]
    p.sort(reverse=True)

    initial_state=(0,) + d

    if sum(initial_state)>n:
        initial_state = reduce_signature(initial_state, n, C)
    
    
    optimal_costs = { initial_state: 0 }
    paths = { initial_state: [] }
    
    
    queue = []
    heapq.heappush(queue, (priority(initial_state,C), initial_state))


    while queue:
        cp,current_signature = heapq.heappop(queue)

        current_m = current_signature[0]
        
        
        new_cost = optimal_costs[tuple(current_signature)] + sum(p[current_m:])
        
        
        shifted_signature = shift_signature(current_signature, C)
        
        
        for q in range(current_signature[1] + 1):
            new_signature = add_to_signature(shifted_signature, q, dv, C)
            
            if sum(new_signature) > n:
                new_signature = reduce_signature(new_signature, n, C)
            
            total_signature = sum(new_signature)
            old_cost=optimal_costs.get(tuple(new_signature))

            if old_cost is None and total_signature!=new_signature[0]:
                heapq.heappush(queue, (priority(new_signature,C), new_signature))
            if old_cost is None or new_cost<old_cost:
                optimal_costs[tuple(new_signature)] = new_cost
                paths[tuple(new_signature)] = paths[tuple(current_signature)] + [q]
    
    final_state = tuple([n]+C*[0])
    path=paths[final_state]

    
    print("Optimal Cost:", optimal_costs[final_state])
    print("Path:", path)
    cb=path_to_cb(path,chars,c)
    print("Codebook:")
    for key in cb:
        print(f'{key}:{cb[key]}')
    print("Elapsed Time:", time.time() - t0)
    return()
    
if __name__ == '__main__':
    main()