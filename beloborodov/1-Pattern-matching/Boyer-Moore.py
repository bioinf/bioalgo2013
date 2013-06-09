from collections import defaultdict
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


def compute_character_last_occur(s):
    bad_character = defaultdict(list)  # ch -> last occ. of character 'ch'.
    for i in range(len(s)-1,-1,-1):
        ch = s[i]
        bad_character[ch].append(i)
    return bad_character

def find_next_char(LastOccur, Symbol, Position, len):
    if LastOccur[Symbol] == []:
        return Position+1
    for i in LastOccur[Symbol]:
        if i < Position:
            return Position-i
    return Position+1

def compute_same_suffix_distance(s):
    n = len(s)
    z = list(reversed(z_array(s[::-1])))
    good_suffix = [n] * n
    for i in range(len(good_suffix)):
        good_suffix[i]=i
    for i in range(n-1,-1,-1):
        good_suffix[-z[i]] = min(n-i-2, good_suffix[-z[i]])
    return good_suffix[1:]+good_suffix[0:1]

def match(s, p):
    lenPattern = len(p)
    i = lenPattern
    same_suffix_distance = compute_same_suffix_distance(p)
    character_last_occur = compute_character_last_occur(p)
    while i <= len(s):
        hope = True
        for j in range(lenPattern-1, -1, -1):
            if s[i-lenPattern+j] != p[j]:
                i += max(1,same_suffix_distance[j],find_next_char(character_last_occur, s[i-lenPattern+j], j, lenPattern))
                hope = False
                break
        if hope:
            yield i-lenPattern
            i += 1

print(list(match('ibababacsbadcba', 'aba')))
