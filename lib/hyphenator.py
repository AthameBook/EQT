"""
This is a Pure Python module to hyphenate text.

Wilbert Berendsen, March 2008
info@wilbertberendsen.nl

License: LGPL.
"""

import sys
import re

__all__ = ("Hyphenator")

hdcache = {}
parse_hex = re.compile(r'\^{2}([0-9a-f]{2})').sub
parse = re.compile(r'(\d?)(\D?)').findall

def hexrepl(matchObj):
    return unichr(int(matchObj.group(1), 16))

class parse_alt(object):
    def __init__(self, pat, alt):
        alt = alt.split(',')
        self.change = alt[0]
        if len(alt) > 2:
            self.index = int(alt[1])
            self.cut = int(alt[2]) + 1
        else:
            self.index = 1
            self.cut = len(re.sub(r'[\d\.]', '', pat)) + 1
        if pat.startswith('.'):
            self.index += 1

    def __call__(self, val):
        self.index -= 1
        val = int(val)
        if val & 1:
            return dint(val, (self.change, self.index, self.cut))
        else:
            return val

class dint(int):
    def __new__(cls, value, data=None, ref=None):
        obj = int.__new__(cls, value)
        if ref and type(ref) == dint:
            obj.data = ref.data
        else:
            obj.data = data
        return obj

class Hyph_dict(object):
    def __init__(self, filename):
        self.patterns = {}
        f = open(filename)
        charset = f.readline().strip()
        if charset.startswith('charset '):
            charset = charset[8:].strip()

        for pat in f:
            pat = pat.decode(charset).strip()
            if not pat or pat[0] == '%':
                continue
            pat = parse_hex(hexrepl, pat)
            if '/' in pat:
                pat, alt = pat.split('/', 1)
                factory = parse_alt(pat, alt)
            else:
                factory = int
            tag, value = zip(*[(s, factory(i or "0")) for i, s in parse(pat)])
            if max(value) == 0:
                continue
            start, end = 0, len(value)
            while not value[start]:
                start += 1
            while not value[end - 1]:
                end -= 1
            self.patterns[''.join(tag)] = start, value[start:end]
        f.close()
        self.cache = {}
        self.maxlen = max(map(len, self.patterns.keys()))

    def positions(self, word):
        word = word.lower()
        points = self.cache.get(word)
        if points is None:
            prepWord = '.%s.' % word
            res = [0] * (len(prepWord) + 1)
            for i in range(len(prepWord) - 1):
                for j in range(i + 1, min(i + self.maxlen, len(prepWord)) + 1):
                    p = self.patterns.get(prepWord[i:j])
                    if p:
                        offset, value = p
                        s = slice(i + offset, i + offset + len(value))
                        res[s] = map(max, value, res[s])

            points = [dint(i - 1, ref=r) for i, r in enumerate(res) if r % 2]
            self.cache[word] = points
        return points

class Hyphenator(object):
    def __init__(self, filename, left=2, right=2, cache=True):
        self.left = left
        self.right = right
        if not cache or filename not in hdcache:
            hdcache[filename] = Hyph_dict(filename)
        self.hd = hdcache[filename]

    def positions(self, word):
        right = len(word) - self.right
        return [i for i in self.hd.positions(word) if self.left <= i <= right]

    def iterate(self, word):
        if isinstance(word, str):
            word = word.decode('latin1')
        for p in reversed(self.positions(word)):
            if p.data:
                change, index, cut = p.data
                if word.isupper():
                    change = change.upper()
                c1, c2 = change.split('=')
                yield word[:p + index] + c1, c2 + word[p + index + cut:]
            else:
                yield word[:p], word[p:]

    def wrap(self, word, width, hyphen='-'):
        width -= len(hyphen)
        for w1, w2 in self.iterate(word):
            if len(w1) <= width:
                return w1 + hyphen, w2

    def inserted(self, word, hyphen='-'):
        if isinstance(word, str):
            word = word.decode('latin1')
        l = list(word)
        for p in reversed(self.positions(word)):
            if p.data:
                change, index, cut = p.data
                if word.isupper():
                    change = change.upper()
                l[p + index: p + index + cut] = change.replace('=', hyphen)
            else:
                l.insert(p, hyphen)
        return ''.join(l)

    __call__ = iterate

if __name__ == "__main__":
    dict_file = sys.argv[1]
    word = sys.argv[2].decode('latin1')
    h = Hyphenator(dict_file, left=2, right=2)

    for i in h(word):
        print(i)
