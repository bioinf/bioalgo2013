def failure_array(a):
    f = [0]*len(a)
    b = 1 # beginning of moving window containing string equals to prefix
    for e in range(1, len(a)):
        if a[e] == a[e - b]:
            f[e] = e - b + 1
        else:
            if a[e] == a[b]:
                f[e] = e - b
                b+=1
            else:
                b = e + 1
    return f

def z_array(a):
    f = [0]*len(a)
    cand = [] # candidates for value of z-function
    for e in range(1, len(a)):
        ae = a[e]
        for i in range(len(cand)-1,-1,-1):
            c = cand[i]
            if ae == a[c]:
                cand[i] += 1
            else:
                f[e-c] = c
                del cand[i]
        if ae == a[0]:
            cand.append(1)
    for c in cand:
        f[-c]=c
    return f

def kmp(s, p, type='prefix'):
    lens, lenp = len(s), len(p)
    if lenp <= lens:
        if type == 'prefix' or type == 'p':
            offset = lenp
            f = failure_array(p + "$" + s)
        else:
            offset = 1
            f = z_array(p + "$" + s)
        return [i for i in range(lens-lenp+1) if f[lenp + offset + i] == lenp]
    else:
        return []

print(kmp('Faster than Sergei's solutions for 10% about :p', 'ab'))
