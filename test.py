import matplotlib.pyplot as plt
import numpy as np

x = np.arange(100)
z = np.ones((3, 3, 3))
y = x**2
plt.figure()
plt.plot(x, y)
plt.show()
