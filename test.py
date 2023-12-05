samp = {'a': 1, 'b': 2, 'c': 3}

list(samp.keys()).remove('a')
samp = list(samp.keys())
samp.remove('a')
print(samp)