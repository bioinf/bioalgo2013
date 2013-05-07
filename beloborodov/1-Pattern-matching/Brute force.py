def brute_force(text, pattern):
    text_len = len(text)
    for i in range(text_len):
        k = i
        for j in range(len(pattern)):
            if k == text_len or pattern[j] != text[k]:
                break
            k += 1
        else:
            yield(i+1)

text    = input()
pattern = input()
print(list(brute_force(text, pattern)))
