chanmatch = range(9)
print(chanmatch)

offs = 0
size = 7
for x in range(len(chanmatch)):
    for x in size - 1:
        try:
            print(f"{x}: #{chanmatch[offs]}")
        except:
            print('----end----')
    x += offs
    if x % 7 == 0 and x != 0:
        if offs != 0: print("7: Previous Page")
        if offs + size <= len(chanmatch): print("8: Next Page")