# JOPy #


JOPy is a port of earlier software, first written in C++ then ported to C#. Those version were in turn supposed to replace older software writen in FORTRAN 77. Not much was left of this origin, but input file format is somewhat similar.

This software loads absorption line data and two additional parameters - namely index of refraction and 2J+1 of fundamental multiplet.
Format of input file is as follows

    2J+1 n
    fexp_1 wavenumber_1 u2_1 u4_1 u6_1 
    fexp_2 wavenumber_2 u2_2 u4_2 u6_2
    ...
    fexp_n wavenumber_n u2_n u4_n u6_n
where 2J+1 is total angular moment of fundamental multiplet, n is index of refraction, fexp_i is i-th experimental oscillator strength and u2_i u4_i u6_i are doubly reduced matrix elements of dipole transition, which can be found in literature.
fexp can be calculated using formula $fexp=4.32*10^{-9} \frac{\int ABS(\nu) d\nu}{c d}$ .