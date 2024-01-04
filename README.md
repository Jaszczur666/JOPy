# JOPy #


JOPy is a port of earlier software, first written in C++ then ported to C#. Those version were in turn supposed to replace older software writen in FORTRAN 77. Not much was left of this origin, but input file format is somewhat similar.
## Input file format ##
This software loads absorption line data and two additional parameters - namely index of refraction and 2J+1 of fundamental multiplet.
Format of input file is as follows

    2J+1 n
    fexp_1 wavenumber_1 u2_1 u4_1 u6_1 
    fexp_2 wavenumber_2 u2_2 u4_2 u6_2
    ...
    fexp_n wavenumber_n u2_n u4_n u6_n
where 2J+1 is total angular moment of fundamental multiplet, n is index of refraction, fexp_i is i-th experimental oscillator strength and u2_i u4_i u6_i are doubly reduced matrix elements of dipole transition, which can be found in literature.
## A bit of theory ##
f<sub>exp</sub> can be calculated using formula $$f_{exp}=4.32*10^{-9} \frac{\int ABS(\nu) d\nu}{c d}$$ where ABS is absorbance, nu is wavenumber in cm<sup>^-1</sup> c is concentration of absorbing ions in mol/L and d is sample thickness in cm.
On the other hand oscillator strength $f_{teor}$ can be calculated using formula
$$f_{teor}= \frac{8 \pi^2 m c }{3 h  \lambda 2J+1} \frac{n(n^2+2)^2}{9} \Sigma_{t=2,4,6} \Omega_t |\langle l^N\Psi J ||U^{(t)} || l^N\Psi\prime J\prime \rangle $$
This enables to fit experimental data by finding the set of $\Omega_t$ values that minimize RMS error. Having those parameters we can also predict the transition rates of all other possible transitions.