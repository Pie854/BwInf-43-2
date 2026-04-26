chars=[]
freq=[]

def shannonfano(chars, freq):
    if len(chars) == 1:
        return [chars[0]]
    else:
        cb = []
        split = [0]
        s = sum(freq)
        rs = 0
        k = 1
        for i in range(len(freq)):
            rs += freq[i]
            if rs >= k * s / base:
                k += 1
                c = abs(rs - k * s / base) < abs(rs - freq[i] - k * s / base)
                split.append(i + 1 if c else i)
        if split[-1] != len(chars):
            split.append(len(chars))
        for i in range(len(split) - 1):
            sub_chars = chars[split[i]:split[i+1]]
            sub_freq = freq[split[i]:split[i+1]]
            sub_codes = shannonfano(sub_chars, sub_freq)
            cb += [str(i) + code for code in sub_codes]
        return cb






def splitcb(cb):
    ch=[]
    co=[]
    for i in cb:
        j=0
        while i[j].isdigit():#s. Huffman
            j+=1
        co.append(i[:j:])
        ch.append(i[j::])
    return(ch,co)

base=int(input())
input()
txt=input()
for c in txt:
    if c in chars:
        freq[chars.index(c)]+=1
    else:
        chars.append(c)
        freq.append(1)

chars=[x for _,x in sorted(zip(freq,chars))][::-1]
freq=sorted(freq)[::-1]



print(chars)
print(freq)


cb=shannonfano(chars,freq)
print(cb)
ch,co=splitcb(cb)
print(ch)
print(co)




tl=0
for i in range(len(ch)):
    tl+=len(co[i])*freq[chars.index(ch[i])]

print(tl)