import timeit
import math
import secant
import newton

x0=0
x1=1
p = lambda x: x**5+x-1
p_prime = lambda x: 5*(x**4)+1

for epsilon in [10**-i for i in range(2,11)]:
    statement1 = "secant.secant(x0,x1,p,epsilon)"
    statement2 = "newton.newton(x0,p,p_prime,epsilon)"
    print(timeit.timeit(statement1, number =1,
        globals = globals()),'/',
    timeit.timeit(statement2, number =1, globals = globals()))
