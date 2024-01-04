from LevMarJO import levenberg_marquardt_fit
from Multiplet import Multiplet

x = Multiplet()
x.load_file("./Test inputs/ErbLGSO_zdeczkapoprawka.in")
print(x)
params = levenberg_marquardt_fit(x)
emi = Multiplet()
emi.load_rate("./Test inputs/amd4i13_2.txt")
emi.n = x.n
emi.calculate_rates(params)
