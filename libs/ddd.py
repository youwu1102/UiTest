__author__ = 'c_youwu'
x =range(10)
x.append(1)
y =[]
def move(z):
    x.remove(z)
    y.append(z)

while True:
    if x:
        print x
        move(x[0])
    else:

        break



