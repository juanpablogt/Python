import matplotlib.pyplot as plt

x_values = list(range(1, 1001))
y_values = [x**2 for x in x_values]

plt.scatter(x_values, y_values, s=1, c=y_values, cmap=plt.cm.Blues,edgecolors='none')

plt.show()