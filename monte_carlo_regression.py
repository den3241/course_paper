import numpy as np
import matplotlib.pyplot as plt


points = [
    (1, 3),
    (2, 5),
    (3, 7),
    (4, 7),
    (5, 12),
    (6, 14)
]


X, y = zip(*points)
X = np.array(X)
y = np.array(y)


n_interations = 50000
best_mse = float('inf')
best_k = None
best_b = None

for i in range(n_interations):
    k = np.random.uniform(-10,10)
    b = np.random.uniform(-10,10)
    y_pred = k*X + b
    mse = np.mean((y - y_pred)**2)

    if mse < best_mse:
        best_mse = mse
        best_k = k
        best_b = b
        print(f"Попытка {i}: k={k}, b={b}, mse={mse}")
        

print("\nРезультат:")
print(f"k = {best_k}")
print(f"b = {best_b}")
print(f"MSE = {best_mse}")

plt.figure(figsize=(8, 5))
plt.scatter(X,y,alpha=0.5,label='Данные')
x_line = np.array([[0], [10]])
y_line = best_k * x_line + best_b
plt.plot(x_line, y_line, 'r-', linewidth=1, label="Найденная прямая")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()