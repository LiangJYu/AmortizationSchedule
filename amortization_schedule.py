'''
source: https://www.boe.ca.gov/info/tvm/lesson7.html
'''

import numpy as np
import matplotlib.pyplot as plt

class Amort:
    def __init__(self, loan_amt, rate, per, extra=0):
        self.apr = rate
        self.ppr = rate / 12
        self.periods = per
        self.extra_payment = extra
        self.amort_payment = 0
        self.balance = np.zeros(per)
        self.balance[0] = loan_amt
        self.interest = np.zeros(per)
        self.cum_interest = np.zeros(per)
        self.principal = np.zeros(per)
        self.cum_principal = np.zeros(per)
        self.calculateAmortPmt()
        self.genAmortSchedule()

    def calculateAmortPmt(self):
        x = (1 + self.ppr) ** self.periods
        self.amort_payment = self.balance[0] * (self.ppr * x) / (x - 1)

    def genAmortSchedule(self):
        i = 0 
        while i < self.periods and self.balance[i] > 0:
            self.interest[i] = self.balance[i] * self.ppr
            self.principal[i] = self.amort_payment - self.interest[i] + self.extra_payment
            if i+1 < self.periods:
                self.balance[i+1] = self.balance[i] - self.principal[i]
            i += 1
        if i < self.periods:
            self.periods = i
            self.balance = self.balance[:i]
            self.interest = self.interest[:i]
            self.principal = self.principal[:i]
        self.cum_interest = np.cumsum(self.interest)
        self.cum_principal = np.cumsum(self.principal)

    def plotIntVsPrin(self):
        plt.close('all')
        for y in [self.principal, self.interest]:
            plt.plot(range(self.periods), y)
        plt.show()


def plot2CumAmorts(a0, a1):
    plt.close('all')
    plt.plot(range(a0.periods), np.cumsum(a0.principal), 'b')
    plt.plot(range(a1.periods), np.cumsum(a1.principal), 'c')
    plt.plot(range(a0.periods), np.cumsum(a0.interest), 'r')
    plt.plot(range(a1.periods), np.cumsum(a1.interest), 'm')
    plt.grid()
    plt.show()


def plot2Amorts(a0, a1):
    plt.close('all')
    plt.plot(range(a0.periods), a0.principal, 'b')
    plt.plot(range(a1.periods), a1.principal, 'c')
    plt.plot(range(a0.periods), a0.interest, 'r')
    plt.plot(range(a1.periods), a1.interest, 'm')
    plt.grid()
    plt.show()


def dt(a0, a1):
    dt = a0.periods - a1.periods
    if dt == 0:
        print('a0 and a1 same period')
    elif dt < 0:
        print(f'a0 faster than a1 by {-dt} periods')
    else:
        print(f'a1 faster than a0 by {dt} periods')


def dpmt(a0, a1):
    dpmt = a0.cum_interest[-1] - a1.cum_interest[-1]
    if dpmt == 0:
        print('a0 and a1 same total interest')
    elif dpmt < 0:
        print(f'a0 less than a1 by {-dpmt}')
    else:
        print(f'a1 less than a0 by {dpmt}')


if __name__ == "__main__":
    import amortization_schedule
    a0 = amortization_schedule.Amort(1e5, 0.06, 360)
    a1 = amortization_schedule.Amort(1e5, 0.06, 360, 100)
    print(a0.amort_payment)
    #a0.plotIntVsPrin()
    dt(a0, a1)
    dpmt(a0, a1)
    plot2Amorts(a0, a1)
    plot2CumAmorts(a0, a1)
