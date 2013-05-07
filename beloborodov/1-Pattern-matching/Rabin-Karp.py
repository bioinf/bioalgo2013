base = 17

def Hash(text):
    length = len(text)
    return sum(base**(length-i-1)*ord(text[i]) for i in range(length))

def RollHash(currentHash, old, length, new):
    newHash = currentHash - base**(length-1) * ord(old)
    newHash *= base
    newHash += ord(new)
    return newHash

def RabinKarp( text, pattern ):
    patternHash = Hash(pattern)
    patternLength = len(pattern)
    iHash = Hash(text[:patternLength])
    if patternHash == iHash:
        yield 0
    for i in range(len(text) - patternLength):
        iHash = RollHash(iHash, text[i],patternLength, text[i+patternLength])
        if patternHash == iHash:
            yield i+1

for hit in RabinKarp('abdsab', 'ab'):
    print(hit)
