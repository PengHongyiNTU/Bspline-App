import matplotlib.pyplot as plt
import numpy as np

def chord_length_parameterization(x, y):
    D = np.stack((x, y), axis=1)
    t = np.zeros(len(D))
    for i in range(1, len(D)):
        t[i] = np.linalg.norm(D[i] - D[i-1])
    t = t.cumsum()
    t = t / t[-1]
    assert t[0] == 0 and t[-1] == 1
    return t

def insert_dummy(t, k):
    T = np.insert(t, 0, [0]*k)
    T = np.append(T, [1]*k)
    return T

def B(u, i, k, T):
    if k == 0:
        if T[i] <= u < T[i+1]:
            return 1.0
        else:
            return 0.0
    if T[i+k] == T[i]:
        c1 = 0.0
    else:
        c1 = (u - T[i]) / (T[i+k] - T[i]) * B(u, i, k-1, T)
    if T[i+k+1] == T[i+1]:
        c2 = 0.0
    else:
        c2 = (T[i+k+1] - u) / (T[i+k+1] - T[i+1]) * B(u, i+1, k-1, T)
    return c1+c2

def derivative(t, func, *args, **kwargs):
    dt = 1e-6
    dy = (func(t + dt, *args, **kwargs) - func(t, *args, **kwargs))
    return dy/dt

def second_derivative(t, func, *args, **kwargs):
    dt = 1e-6
    dy = derivative(t+dt, func, *args, **kwargs) - derivative(t, func, *args, **kwargs)
    return dy/dt

def get_N(k, t, T):
    n = len(t)-1
    N = np.zeros((n+3, n+3))
    for i in range(2, n+1):
        for j in range(i-1, i+2):
            N[i, j] = B(t[i-1], j, k, T)
            # print(f'N[{i}, {j}] = {N[i, j]}')
    N[0, 0] = 1.0
    N[n+2, n+2] = 1.0
    for i in range(0, 3):
        N[1, i] = second_derivative(t[0], B, i, k, T)
    for i in range(n, n+3):
        N[n+1, i] = second_derivative(t[n]-1e-5, B, i, k, T)
    return N

def get_D(x, y):
    D = np.stack((x, y), axis=1)
    D = np.insert(D, 1, [0, 0], axis=0)
    D = np.insert(D, len(D)-1, [0, 0], axis=0)
    return D

def bspline(u, P, k, T):
    n = len(T) - k -1
    assert (n >= k+1) and (len(P)>=n)
    return sum(P[i]*B(u, i, k, T) for i in range(n))

def get_P(N, D):
    P = np.linalg.solve(N, D)
    return P

def get_curve(P, k, T):
    return np.array([bspline(x, P, k, T) for x in np.arange(0, 1, 0.01)])

if __name__ == "__main__":
    x = [0, 0, 2, 2, 4]
    y = [0, 2, 2, 0, 0]
    k = 3
    t = chord_length_parameterization(x, y)
    T = insert_dummy(t, k)
    N = get_N(k, t, T)
    D = get_D(x, y)
    P = get_P(N, D)
    curve = get_curve(P, k, T)
    plt.plot(P[:, 0], P[:, 1], '--k', label='Control Polygon', marker='s', markersize=5)
    plt.scatter(x=x, y=y, c='r', s=80, label='Data Points')
    plt.plot(curve[:, 0], curve[:, 1], 'b', linewidth=2, label='B-spline curve')
    plt.legend()
    plt.title('Cubic B-spline curve')
    plt.show()
