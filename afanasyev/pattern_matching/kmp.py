seq = open('D:\\temp\\my.txt', 'r').readline()
seq = seq.replace('\n', '')
seq = seq.replace('\r', '')

out = list([0])
i = 1
j = 0
while i < len(seq):
    if seq[i] == seq[j]:
        while i < len(seq) and seq[i] == seq[j]:
            j += 1
            i += 1
            out.append(j)
        j = out[j-1]
    else:
        j = 0
        out.append(0)
        i += 1

f = open('D:\\temp\\my2.txt', 'w')
for i in out:
    f.write(str(i) + ' ')

f.close()
