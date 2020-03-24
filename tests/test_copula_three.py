#!/usr/bin/python3.8

from rediz.client import Rediz
import time
from rediz.rediz_test_config import REDIZ_TEST_CONFIG
import numpy as np
from pprint import pprint
from scipy.integrate import odeint
from math import sqrt


NAMES = ['three_body_x.json','three_body_y.json','three_body_z.json']
SCALE = 10**8
Y0  = [384.6 * 10 ** 6, 0, 0, 1197000, -9928000, 0, 0, 1025, 0, 8490, -2455, 100]
print("Initial value is " + str( [y/SCALE for y in Y0[:3] ]), flush=True)
Y   = Y0


def threebody(Y,t):
    """
       Forked from https://guillaumecantin.pythonanywhere.com/animation/4/
    """
    m1 = 5.974 * 10 ** 24  # Earth
    m2 = 7.348 * 10 ** 22  # Moon
    m3 = 10000             # Spaceship
    g = 6.672 * 10 ** (-10)  # gravitational constant .. should be -11

    def r(x, y, z):
        return sqrt(x * x + y * y + z * z)

    def f(x, y, b, c, d1, d2, d3):
        return -g * (m1 + b) * x / (d1 ** 3) + g * c * ((y - x) / (d2 ** 3) - y / (d3 ** 3))

    dY = [0 for i in range(12)]
    dY[0] = Y[6]
    dY[1] = Y[7]
    dY[2] = Y[8]
    dY[3] = Y[9]
    dY[4] = Y[10]
    dY[5] = Y[11]
    r12 = r(Y[0], Y[1], Y[2])
    r23 = r(Y[0] - Y[3], Y[1] - Y[4], Y[2] - Y[5])
    r13 = r(Y[3], Y[4], Y[5])
    dY[6] = f(Y[0], Y[3], m2, m3, r12, r23, r13)
    dY[7] = f(Y[1], Y[4], m2, m3, r12, r23, r13)
    dY[8] = f(Y[2], Y[5], m2, m3, r12, r23, r13)
    dY[9] = f(Y[3], Y[0], m3, m2, r13, r23, r12)
    dY[10] = f(Y[4], Y[1], m3, m2, r13, r23, r12)
    dY[11] = f(Y[5], Y[2], m3, m2, r13, r23, r12)
    return dY


def evolve():
    global Y
    time = np.arange(0, 0.02*265600, 1)
    orbit = odeint(threebody, Y, time)
    x, y, z, a, b, c, dx, dy, dz, da, db, dc = orbit.T
    values = [ x[-1]/SCALE, y[-1]/SCALE, z[-1]/SCALE ]
    noise  = [ 0.1*np.random.randn() for v in values ]
    noisy_values = [ v + n for v,n in zip(values,noise ) ]
    rdz = Rediz(**REDIZ_TEST_CONFIG)
    budgets = [ 10., 10., 10. ]
    res = rdz.cset(names=NAMES, write_key=REDIZ_TEST_CONFIG['write_key'], values=noisy_values, budgets=budgets)

def test_three_body():
    # Fail fast ...
    evolve()
    time.sleep(1)
    evolve()






