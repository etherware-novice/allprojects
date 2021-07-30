import textwrap
from itertools import zip_longest

def split_bar(right, left):
    txt_width = 10


    l_d = ""
    for l, r in zip(left, right):
        r = textwrap.fill(r, width=txt_width).splitlines()
        l = textwrap.fill(l, width=txt_width).splitlines()
        
        for x, y in zip_longest(l, r, fillvalue=""):
            yield f"{x.rjust(txt_width)} ! {y.ljust(txt_width)}"

right = ["stringgggggggg", "str2", "*"]
left = ["this is a very long string for testing", "user", "#3"]

for x in split_bar(left, right):
    pass
    #print(x)


l0 = "time"
l1 = "chn"
l2 = "usr"

l_disp = f"{l0} ! {l1.center(10)} ! {l2}"
r = "a str"

out = f" {l_disp.rjust(30)} ! {r.ljust(20)}"
print(out)
