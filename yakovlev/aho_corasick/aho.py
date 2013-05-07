from copy import deepcopy

_start = "#"
_end = "$"

_rootnum = 1

_default = [{},_rootnum,None,[]]
_dictpos = 0
_numpos = 1
_suffpos = 2
_pattpos = 3

_root = { _start : deepcopy(_default) }


def get_dict( trie_node, arg ):
    return trie_node[arg][_dictpos]

def get_num( trie_node, arg ):
    return trie_node[arg][_numpos]

def get_suff( trie_node, arg ):
    return trie_node[arg][_suffpos]

def get_patt( trie_node, arg ):
    return trie_node[arg][_pattpos] 

def get_or_create_node( trie_node, arg, number = _rootnum ):
    t = deepcopy(_default)
    t[_numpos] = number
    return trie_node.setdefault(arg, t)

def get_end_node( trie_node ):
    return trie_node.setdefault(_end, _end)

def append_pattern( trie_tnode, pattern ):
    trie_tnode[_pattpos].append(pattern)

def get_max_number( trie ):
    current_dict = get_dict(trie, _start)
    _max = _rootnum
    check = [current_dict]
    while check:
        next_check = []
        for dic in check:
            for i in dic:
                if i == _end:
                    continue
                n = get_num(dic, i)
                _max = max(_max, n)
                next_check.append(get_dict(dic, i))
        check = next_check
    return _max

def insert_trie( words, trie = deepcopy(_root) ):
    tr = deepcopy(trie)
    _max = get_max_number(tr)
    root = get_dict(tr, _start)
    for word in words:
        current_dict = root
        for letter in word:
            current_tup = get_or_create_node(current_dict, letter, _max + 1)
            current_dict = current_tup[_dictpos]
            _max += 1
        append_pattern(current_tup, word)
        current_dict = get_end_node(current_dict)
    return tr

def wave_print( letter, from_n, in_n, tuple = [] ):
    print from_n, in_n, letter

def wave_trie( trie, wave_operation = wave_print ):
    check = [trie[_start]]
    while check:
        next_check = []
        for tup in check:
            n = tup[_numpos]
            s = tup[_suffpos]
            dic = tup[_dictpos]
            for i in dic:
                if i == _end:
                    continue
                next_check.append(dic[i])
                ni = get_num(dic,i)
                wave_operation(i,n,ni)
                si = get_suff(dic, i)
                wave_operation('S',ni,si[_numpos] if si != None else -1)
        check = next_check

def contains( trie, word ):
    current_dict = get_dict(trie, _start)
    for letter in word:
        if letter in current_dict:
            current_dict = get_dict(current_dict, letter)
        else:
            return False
    if _end in current_dict:
        return True
    return False

def initiate_suffix_links( trie ):
    root = trie[_start]
    queue = []
    for node in root[_dictpos].itervalues():
        queue.append(node)
        node[_suffpos] = root

    while queue:
        rnode = queue.pop(0)

        for key, node in rnode[_dictpos].iteritems():
            if key == _end:
                continue
            queue.append(node)
            fnode = rnode[_suffpos]
            while fnode != None and key not in fnode[_dictpos]:
                fnode = fnode[_suffpos]
            node[_suffpos] = fnode[_dictpos][key] if fnode else root
            node[_pattpos] += node[_suffpos][_pattpos]

    return trie

def aho_corasik( text, pattern_list ):
    result = { p : [] for p in pattern_list }
    t = insert_trie(pattern_list)
    initiate_suffix_links(t)
    node = t[_start]
    for i in xrange(len(text)):
        while node != None and text[i] not in node[_dictpos]:
            node = node[_suffpos]
        if node == None:
            node = t[_start]
            continue
        node = node[_dictpos][text[i]]
        for pattern in node[_pattpos]:
            result[pattern].append(i - len(pattern) + 1)
    return result

def rosalind():
    l = []
    while True:
        try:
            c = raw_input()
            l.append(c)
        except:
            break

    t = insert_trie(l)
    initiate_suffix_links(t)

    wave_trie(t)

def getstrbynum( alpha, num ):
    result = []
    lalpha  = [''] + list(alpha)
    n = num - 1

    while True:
        result.append(lalpha[n % 4 + 1])
        n /= 4
        n -= 1
        if n < 0:
            break
    return "".join(result[::-1])

def makePatternList( pattern_list_list ):
    r = []
    for pattern_list in pattern_list_list:
        first = pattern_list[0]
        last = pattern_list[1]
        step = pattern_list[2]
        for i in xrange(first, last, step):
            r.append(getstrbynum("ACGT", i))
    return r

def rosalindEPM():
    text = raw_input()
    pll = []
    while True:
        try:
            s = raw_input()
            pll.append([int(s) for s in s.strip().split()])
        except:
            break

    pattern_list = makePatternList(pll)
    res = aho_corasik(text, pattern_list)
    for pattern in res:
        for r in res[pattern]:
            print r+1,

def main():
    #text = raw_input()
    #pattern_list = raw_input().split()

    #res = aho_corasik(text, pattern_list)
    #for pattern in res:
    #    print pattern, res[pattern]
    rosalindEPM()

if __name__ == "__main__":
    main()
