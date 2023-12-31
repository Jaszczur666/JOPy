import re

import numpy as np

pi = np.pi
m = 9.1093897e-28
c = 2.99792458e10
h = 6.6260755e-27
qe = 4.8032068e-10


class Line:
    def __init__(self, f, wn, u2, u4, u6):
        if f is not None:
            self.f = float(f)
        else:
            self.f = None
        self.wn = float(wn)
        self.u2 = float(u2)
        self.u4 = float(u4)
        self.u6 = float(u6)

    def __str__(self):
        if self.f is not None:
            stringrep = f"{self.f:.5} {int(self.wn): 5d} {self.u2:.4} {self.u4:.4} {self.u6:.4}\n"
        else:
            stringrep = f"{int(self.wn): 5d} {self.u2:.4} {self.u4:.4} {self.u6:.4}\n"

        return (
                stringrep
        )


class EmLine:
    def __init__(self, wn, u2, u4, u6):
        self.wn = np.longdouble(wn)
        self.u2 = np.longdouble(u2)
        self.u4 = np.longdouble(u4)
        self.u6 = np.longdouble(u6)

    def __str__(self):
        return f"{int(self.wn): 5d} {self.u2:.4} {self.u4:.4} {self.u6:.4}\n"


def oscillator_strength(line, n, tjpo, o2, o4, o6):
    #   print(type(n))
    # print(f"{line} n=  {n} {tjpo} {o2} {o4} {o6}")
    wl = 1 / line.wn
    top = (((n**2.0 + 2) ** 2.0) / (9 * n)) * 8 * (pi**2) * m * c
    bottom = 3 * h * tjpo * wl
    return (top / bottom) * (o2 * line.u2 + o4 * line.u4 + o6 * line.u6)


class Multiplet:
    def add_line(self, line):
        self.lines.append(line)

    def add_emline(self, emline):
        self.lines.append(emline)

    def load_file(self, fname):
        print(f"Loading {fname}")
        with open(fname) as f:
            lines = [line.strip("\n") for line in f]
        (twojplusone, n) = lines[0].split(" ")
        self.n = np.longdouble(n)
        self.tjpo = np.longdouble(twojplusone)
        for i in range(1, len(lines)):
            pattern = re.compile(
                "^(?P<f>[0-9.E+-]+) (?P<wn>[0-9.]+)" +
                " (?P<u2>[0-9.]+) (?P<u4>[0-9.]+) (?P<u6>[0-9.]+) ?(?:#amd=(?P<amd>[0-9.]+))?",
                re.I,
            )
            match = pattern.search(lines[i])
            # (f, wn, u2, u4, u6) = lines[i].split(" ")
            (f, wn, u2, u4, u6) = (
                match.groupdict()["f"],
                match.groupdict()["wn"],
                match.groupdict()["u2"],
                match.groupdict()["u4"],
                match.groupdict()["u6"],
            )
            self.add_line(Line(f, wn, u2, u4, u6))

    def load_rate(self, fname):
        print("________________________________________")
        print(f"Loading emission data from {fname}")
        with open(fname) as f:
            lines = [line.strip("\n") for line in f]
        twojplusone: int
        (twojplusone, n) = lines[0].split(" ")
        self.n = np.longdouble(n)
        self.tjpo = np.longdouble(twojplusone)
        pattern = re.compile(
            "^(?P<wn>[0-9.]+) (?P<u2>[0-9.]+) (?P<u4>[0-9.]+) (?P<u6>[0-9.]+) ?(?:#amd=(?P<amd>[0-9.]+))?"
        )
        for i in range(1, len(lines)):
            # (wn, u2, u4, u6) = lines[i].split(" ")
            match = pattern.search(lines[i])
            # print (match.groupdict()["wn"])
            (wn, u2, u4, u6) = (
                match.groupdict()["wn"],
                match.groupdict()["u2"],
                match.groupdict()["u4"],
                match.groupdict()["u6"],
            )
            if match.groupdict()["amd"] is not None:
                self.amd = self.n**3 * np.longdouble(match.groupdict()["amd"])
                # print(f'Magnetic dipole contribution to transition rate is {self.amd}')
            self.add_line(Line(None, wn, u2, u4, u6))
        print(self)

    def calculate_rates(self, parameters):
        rates = []
        sumrate = 0
        for line in self.lines:
            rate = (
                (64 * pi**4 * qe**2)
                / (3 * h * (line.wn**-3) * self.tjpo)
                * (self.n * (self.n**2 + 2) ** 2 / 9)
                * (
                    line.u2 * parameters[0]
                    + line.u4 * parameters[1]
                    + line.u6 * parameters[2]
                )
            )
            sumrate += rate
            rates.append(rate)
        print("Wavenumber wavelength rate branching ratio %")
        for i in range(len(self.lines)):
            print(
                f"{int(self.lines[i].wn)} {1e7 / self.lines[i].wn:.1f} {rates[i]:.5} {100 * rates[i] / sumrate:.4}"
            )
        print("________________________________________")
        print(
            f"Total rate         {sumrate:.1f} s^-1 {1e6 / sumrate:.0f} us  or {1e3 / sumrate:.2f} ms"
        )
        if self.amd is not None:
            sumrate += self.amd
            print(
                f"Total rate with MD {sumrate:.1f} s^-1 {1e6 / sumrate:.0f} us  or {1e3 / sumrate:.2f} ms"
            )
            print(f"Magnetic dipole contribution to transition rate is {self.amd:.5}")

    def __init__(self):
        self.amd = None
        self.lines = []
        self.n = 1.234
        self.tjpo = 2
        self.is_fitted = False

    def __str__(self):
        strlines = ""
        for line in self.lines:
            strlines += str(line)
        return (
            "Multiplet with 2j+1 = "
            + str(self.tjpo)
            + " and n= "
            + str(self.n)
            + "\n"
            + strlines
        )
