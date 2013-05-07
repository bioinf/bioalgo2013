class Node:
    def __init__(self, children=[], parent=None, symbol=None, out=[], fall=None):
        self.children = children
        self.parent = parent
        self.out = out
        self.symbol = symbol
        self.fall = fall

patterns = ['abc', 'bca', 'cab', 'acb', 'a']
text = 'abcabcacbbcacbaacbabc'

root = Node()
for p in patterns:
    current = root
    for c in p:
        find = False
        for child in current.children:
            if child.symbol == c:
                current = child
                find = True
                break
        if find == False:
            newnode = Node([], current, c, [])
            current.children.append(newnode)
            current = newnode
    current.out = [p]

que=[]
for child in root.children:
    child.fall = root
    que += child.children
while len(que) > 0:
    find = False
    current_fall = que[0].parent
    while not find:
        current_fall = current_fall.fall
        for alt in current_fall.children:
            if alt.symbol == que[0].symbol:
                que[0].fall = alt
                if alt.out:
                    que[0].out += alt.out
                find = True
                break
        if que[0].parent.fall == root and find == False:
            que[0].fall = root
            find = True
    que += que[0].children
    del que[0]

current = root
for i in range(len(text)):
    find = False
    while not find:
        for child in current.children:
            if child.symbol == text[i]:
                current = child
                find = True
                break
        if not find:
            if current == root:
                break
            current = current.fall
    for o in current.out:
        print(i-len(o)+1, o)
