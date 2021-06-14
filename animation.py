import os

ls = os.listdir()

if not 'new' in ls:
    os.mkdir('new')

for name in ls:
    xd, yd = -1, -1
    if not '.csv' in name:
        continue
    f = open(name, 'r')
    f_new = open("new/" + name, 'w')

    i = 0
    for line in f:
        g = line
        line_last = line.split(',')
        line = line_last[1:3]
        if len(line) != 2:
            f_new.write(g)
            continue
        i += 1
        x, y = map(float, line)
        if i == 1:
            xd = x
            yd = y
        x -= xd
        y -= yd
        line_last[1] = str(round(x, 4))
        line_last[2] = str(round(y ,4))
        text = ""
        print(','.join(line_last))
        f_new.writelines(','.join(line_last))
    f.close()
    f_new.close()
