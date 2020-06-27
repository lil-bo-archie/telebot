
l1 = ['roma','archie', 'yuko', 'yura']
d = 0
while True:
    if d >= len(l1):
        d = 0
    s = int(input('input 1 or 0: '))
    # print(s)
    if s == 1:
        d = d+1
        # print(d)
    print(l1[d-1],'cleans')
