import numpy as np
import scipy
import matplotlib.pyplot as plt

temps = np.load('temperatures.npy')  # reel ; V_exp
# print(temps)

temp_reel = temps[:, 0]
# print(temp_reel)

v_exp = temps[:, -1]
# print(v_exp)

temp_exp = 10 * v_exp - 10
# print(temp_exp)

# print(len(temp_reel))  #72 temperatures
rmse = np.sqrt((np.sum((10 * v_exp - 10 - temp_reel) ** 2)) / len(temp_reel))
# print(rmse) #out: 2.4%

v_lisse = scipy.signal.medfilt(v_exp)
# print(v_exp)
# print(v_lisse)

temp_lisse = 10 * v_lisse - 10


def courbe():
    plt.plot(temp_reel, label='real')
    plt.plot(temp_exp, label='exp')
    plt.plot(temp_lisse, label='lisse')
    plt.ylabel('Temperature')
    plt.xlabel('Time')
    plt.title('T°=f(t)')
    plt.legend()
    plt.show()


def hist():
    # print(temp_exp.max().round())
    bin = int(temp_exp.max().round()) + 1
    plt.hist(temp_exp, bins=bin)
    plt.hist(temp_lisse, bins=bin)
    plt.xlabel('Temperature')
    plt.ylabel('occurences')
    plt.show()

# courbe()
# hist()

a=np.ones(10)
plt.hist(a, bins=45)
plt.show()