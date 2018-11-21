#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import linspace as linspace
from scipy import integrate
import math

def beta(NA, g, n1, l, core_d, clad_d, m, p):

  def n(r):
    if r >=0 and r <= a:
      return n1 * math.sqrt(1 - 2 * delta * ((r / a)**g))
    else:
      return n1 * math.sqrt(1 - 2 * delta)
  
  def f(r):
    if r == 0:
      return 0
    val = (ko**2) * (n(r)**2) - (b**2) - m**2 / (r**2)
    if val <= 0:
      return 0
    return math.sqrt(val)
  
  core_r = core_d / 2
  clad_r = clad_d / 2
  a = core_r
  ko = (2 * math.pi) / l 
  v = (2 * math.pi * a * NA)/l
  delta = (NA**2) / (2 * (n1**2))
  n2 = n(1)
  upper_b = n1*ko
  lower_b = n2*ko

  B = linspace(lower_b, upper_b, 500) #testowane wartosci b
  
  r_best = 0
  lowest_areadiff = 99999
 
  for beta in B: #calka dla kazdej testowanej wartosci b
    b = beta
    area = integrate.quad(f,0,clad_r)[0]

    dif = abs(p*math.pi - area)
    if dif < lowest_areadiff:
      r_best = b
      lowest_areadiff = dif

  if not (ko*n1 > r_best > ko*n2):
    raise ValueError("Calculated bad value")

  return { "areadiff": lowest_areadiff, "b": r_best, "v": v, "ko": ko, "l": l}



if __name__ == "__main__":
  print(beta(0.2, 2, 1.482, 850e-9, 0.000050, 0.000125, 0, 1))
