import numpy as np
from numpy.linalg import inv, cond
import matplotlib.pyplot as plt
from Multiplet import F, line

# from math import *


# STALE m = 9.1093897e-28 c = 2.99792458e10 h = 6.6260755e-27 qe = 4.8032068e-10
def chi2(multiplet, params):
    chi2 = 0
    for line in multiplet.lines:
        chi2 += (residue(line, multiplet.n, multiplet.tjpo, params)) ** 2
    return chi2


def residue(line, n, tjpo, params):
    return np.longdouble(line.f) - F(
        line, n, tjpo, params[0], params[1], params[2]
    )  # fitfun(x, params)


def fitfun(x, params):
    return params[0] * np.exp(-(x / params[1])) + params[2]


def CalculateMatrices(multiplet, params):
    delta = np.longdouble(1e-25)
    R = np.zeros(len(multiplet.lines))
    Jaco = np.zeros((len(multiplet.lines), 3))
    for i in range(len(multiplet.lines)):
        R[i] = residue(multiplet.lines[i], multiplet.n, multiplet.tjpo, params)
        for j in range(params.shape[0]):
            dPar = np.zeros(params.shape[0])
            dPar[j] = delta
            # print(f"{(residue(multiplet.lines[i],multiplet.n,multiplet.tjpo,params + dPar))} , R[i]={R[i] } {params} {dPar}")
            Jaco[i, j] = np.longdouble(
                (
                    residue(
                        multiplet.lines[i], multiplet.n, multiplet.tjpo, params + dPar
                    )
                    - R[i]
                )
                / delta
            )
    # print(f" Jakobian {Jaco} natomiast R {R}")
    Hess = np.matmul(Jaco.T, Jaco)
    Grad = np.matmul(Jaco.T, R)
    return (Hess, Grad, R)


def LevMar(dane):
    params = np.array([1e-20, 2e-20, 3e-20])
    lam = 1 / 1024.0
    print("Step number o2 o4 o6 chi2")
    for j in range(10):
        (Hess, Grad, R) = CalculateMatrices(dane, params)
        # print (f"R= {R}")
        Hessd = np.diag(
            np.diag(Hess)
        )  # Macierz ktora ma elementy hessianu na przekatnej a zere poza
        currChi2 = np.matmul(R.T, R)
        # print(f"hesjan jego taka {Hess}, a conditional {cond(Hess)}")
        nparams = params - np.matmul(inv(Hess + lam * Hessd), Grad)
        # print(chi2(dane, nparams), currChi2)
        if chi2(dane, nparams) < currChi2:
            params = nparams
            lam = lam * 1.8
        else:
            lam = lam / 3.8
        print(
            j + 1,
            f"{params[0]:.5} {params[1]:.5} {params[2]:.5}",
            "{:2.5e}".format(chi2(dane, params)),
        )
        if lam < 1e-26:
            break
    for line in dane.lines:
        tf = F(line, dane.n, dane.tjpo, params[0], params[1], params[2])
        print(
            f"{int(line.wn)} {1e7/line.wn:.1f} {line.f:.5} {tf:.5} { 100*(line.f-tf)/line.f:.2f}%"
        )
    dane.is_fitted = True
    return params


if __name__ == "__main__":
    decay = np.loadtxt("dane.dat", comments="#", delimiter=" ", unpack=False)
    params = LevMar(decay)
    plt.plot(decay[:, 0], decay[:, 1])
    x = decay[:, 0]
    plt.plot(x, fitfun(x, params))
    plt.yscale("log")
    plt.show()
    print("Fit parameters are", params)
    input("Ciepnijwa entera coby skonczyc")