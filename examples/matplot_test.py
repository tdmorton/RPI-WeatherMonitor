import matplotlib.pyplot as plt

mlist = [3.1]

print(mlist)

mlist.append(4.2)

print(mlist)

mlist.append(5.3)

print(mlist)

mlist.append(6.4)
mlist.pop(0)

print(mlist)

plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.savefig('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/testfigaa.png')
