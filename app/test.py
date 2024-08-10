c = '==='

for index, i in enumerate(c):
    if i == '=' and index < 2 and c[index + 1] == '=':
        print(1)