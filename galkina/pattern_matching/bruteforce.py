# -*- coding: utf-8 -*-

def brute_force(text, pattern):
    result = []
    for i in xrange(len(text)):
        if text[i] == pattern[0]:
            for j in xrange(len(pattern)):
                if i + j == len(text) or text[i + j] != pattern[j]:
                    break
                elif j == len(pattern):
                    result.append(i)
    return result