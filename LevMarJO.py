import numpy as np
from numpy.linalg import inv

from Multiplet import oscillator_strength


def chi2(multiplet, params):
    chi2_value = 0
    for line in multiplet.lines:
        chi2_value += (residue(line, multiplet.n, multiplet.tjpo, params)) ** 2
    return chi2_value


def residue(line, n, tjpo, params):   # tjpo for two j plus one or 2J+1
    return float(line.f) - oscillator_strength(
        line, n, tjpo, params[0], params[1], params[2]
    )


def calculate_matrices(multiplet, params):
    delta = np.longdouble(1e-25)
    residue_vector = np.zeros(len(multiplet.lines))
    jacobian = np.zeros((len(multiplet.lines), 3))
    for i in range(len(multiplet.lines)):
        residue_vector[i] = residue(multiplet.lines[i], multiplet.n, multiplet.tjpo, params)
        for j in range(params.shape[0]):
            d_par = np.zeros(params.shape[0])
            d_par[j] = delta
            jacobian[i, j] = np.longdouble(
                (
                    residue(
                        multiplet.lines[i], multiplet.n, multiplet.tjpo, params + d_par
                    )
                    - residue_vector[i]
                )
                / delta
            )
    hess = np.matmul(jacobian.T, jacobian)
    grad = np.matmul(jacobian.T, residue_vector)
    return hess, grad, residue_vector


def levenberg_marquardt_fit(dane):
    params = np.array([1e-20, 2e-20, 3e-20])
    hessd = np.array([1, 1, 1])  # Initialization with bogus values just in case
    curr_chi2 = 0
    lam = 1 / 1024.0
    print("Step number o2 o4 o6 chi2")
    for j in range(10):
        (hess, grad, r) = calculate_matrices(dane, params)
        hessd = np.diag(
            np.diag(hess)
        )  # Matrix having same diagonal as Hessian, but zeroes everywhere else
        curr_chi2 = np.matmul(r.T, r)
        nparams = params - np.matmul(inv(hess + lam * hessd), grad)
        if chi2(dane, nparams) < curr_chi2:
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
    error = np.sqrt(np.diag(inv(hessd)) * curr_chi2 / (len(dane.lines) - 3))
    print("______________________________________________")
    print(
        f"Judd Ofelt intensity parameters are: \n O2= {params[0]:.3} O4= {params[1]:.3} O6 ={params[2]:.3}"
    )
    print(f"Errors are dO2 {error[0]:.3} do4 {error[1]:.3} do6 {error[2]:.3}")
    print(
        f"Relative errors are dO2/O2 {100*error[0]/params[0]:.3}%" +
        f"dO4/O4 {100*error[1]/params[1]:.3}% dO6/O6 {100*error[2]/params[2]:.3} %"
    )
    print("______________________________________________")
    print("Wavenumber wavelength fexp fteor (fexp-fteor)/fexp [%]")
    sum_of_squares = 0
    sum_of_strengths = 0
    for line in dane.lines:
        tf = oscillator_strength(
            line, dane.n, dane.tjpo, params[0], params[1], params[2]
        )
        print(
            f"{int(line.wn)} {1e7/line.wn:.1f} {line.f:.5} {tf:.5} {100*(line.f-tf)/line.f:.2f}%"
        )
        sum_of_squares += (line.f - tf) ** 2
        sum_of_strengths += line.f
    size = len(dane.lines) - 3
    print("______________________________________________")
    print(
        f"RMS error is {np.sqrt(sum_of_squares/size):.3}" +
        f" RMS/avg f {100*np.sqrt(sum_of_squares/size)/sum_of_strengths:.1f} %"
    )
    dane.is_fitted = True
    print("______________________________________________")
    return params
