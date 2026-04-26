import time

def trtocb(tree:list):
    if len(tree)==1:
        return([tree[0]],[[]])
    else:
        letters=[]
        codes=[]
        for i in range(base):
            l,c = trtocb(tree[i])
            for j in range(len(l)):
                letters.append(l[j])
                code=c[j]
                code=[i]+code
                codes.append(code)
        return(letters,codes)



chars=[]
freq=[]

#Input: O(1)

base=int(input())
input()
txt=input()

t0=time.time()

#Häufigkeiten zählen: O(n)

for c in txt:
    if c in chars:
        freq[chars.index(c)]+=1
    else:
        chars.append(c)
        freq.append(1)

print(f"Häufigkeiten zählen: {time.time()-t0}")

#Sortieren: O(d log d)

chars=[x for _,x in sorted(zip(freq,chars))][::-1]
freq.sort(reverse=True)

print(f"Sortieren: {time.time()-t0}")
print(freq)


#Initialisierung: O(1)
dc=0 #Dummycounter

#Dummies adden: O(b)
while len(freq)%(base-1)!=1 and base!=2:
    chars.append('dummy'+str(dc))
    freq.append(0)
    dc+=1

print(f"Dummies: {time.time()-t0}")


#Huffman base n: ca. O((d + dc) * (log d) / b)
nodes=[[i] for i in chars]
nodef=freq.copy()

while len(nodes)>base: #(d+dc)/(b-1) Iterationen
    newnode=[]
    f=0
    for i in range(base): #Entfernen der Knoten: O(b)
        newnode.append(nodes.pop())
        f+=nodef.pop()
    k=0
    #Einsortieren an der richtigen Stelle: O(log d) (avg. case)
    while k<len(nodef) and f<nodef[k]: #TODO: cleaner (Immer Intervall halbieren)
        k+=1
    nodef.insert(k,f)
    nodes.insert(k,newnode)

print(f"Huffman: {time.time()-t0}")

#Tree to codebook: O(k)
letters,codes=trtocb(nodes)

print(f"Tree to codebook: {time.time()-t0}")

#Gesamtlänge berechnen: O(k)
tl=0
for i in range(len(codes)):
    tl+=len(codes[i])*freq[chars.index(letters[i])]

print(f"Final: {time.time()-t0}")
print(tl)

