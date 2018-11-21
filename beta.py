#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import linspace as linspace
from math import sqrt as sqrt
import math
import numpy as np
from scipy import integrate


def przypadek(NA, g, n1, l, core_d, clad_d, m, p):

  def n(r):
    if r >=0 and r <= a:
      return n1 * sqrt(1 - 2 * delta * ((r / a)**g))
    else:
      return n1 * sqrt(1 - 2 * delta)
  
  def f(r):
    if r == 0:
      return 0
    val = (ko**2) * (n(r)**2) - (b**2) - m**2 / (r**2)
    if val <= 0:
      return 0
    return sqrt(val)
  
  core_r = core_d / 2
  clad_r = clad_d / 2
  a = core_r
  ko = (2 * math.pi) / l 
  v = (2 * math.pi * a * NA)/l
  delta = (NA**2) / (2 * (n1**2))
  n2 = n(1)
  upper_b = n1*ko
  lower_b = n2*ko

  B = np.linspace(lower_b, upper_b, 500) #testowane wartosci b
  
  #r = np.arange(0.0, clad_r, 1e-7)
  #y = [ n(x) for x in r ] 
  #N = 10000 #liczba przedzialow calkowania
  #li = np.linspace(0, clad_r, 10000)[1:]
  
  #A = []
  #i = 0
  r_best = 0
  lowest_areadiff = 99999
 
  for beta in B: #calka dla kazdej testowanej wartosci b
    b = beta
    area = integrate.quad(f,0,clad_r)[0]

    dif = abs(p*math.pi - area)
    if dif < lowest_areadiff:
      r_best = b
      lowest_areadiff = dif

  #print(ko*n1, r_best, ko*n2)
  if not (ko*n1 > r_best > ko*n2):
    print("bad b")
  return { "areadiff": lowest_areadiff, "b": r_best, "v": v, "ko": ko, "l": l}
  

  #NA = 0.2
  #g=2
  #n1 = 1.482
  #l = 1550e-9
  #core_d = 0.000050


wynik = przypadek(0.2, 2, 1.482, 850e-9, 0.000050, 0.000125, 0, 1)

print(wynik)
print("\n")
print("Beta: {}".format(wynik['b']))
print("\n")



exit(0)
print("test")
fale = np.linspace(850e-9, 1300e-9, 30)
mody = [(0,1), (1,1), (2,1), (0,2), (3,1)]
wyniki = []

vals01 = []
vals11 = []

for mod in mody:
  wyniki_modu = []
  for fala in fale:
    wyniki_modu.append( przypadek(0.2, 2, 1.482, fala, 0.000050, 0.000125, mod[0], mod[1]) ) 
  wyniki.append(wyniki_modu)

for wynik in wyniki:
  wynik.reverse()
  x = [val["v"] for val in wynik]
  #x = [val["v"]/sqrt(2) for val in wynik]
  y = [val["b"] / val["ko"] for val in wynik]
  plt.plot(x,y)

plt.show() 
#for fala in fale:
#  for mod in mody:
#
#  vals01.append( przypadek(0.2, 2, 1.482, fala, 0.000050, 0.000125, 0, 1) )
#  vals11.append( przypadek(0.2, 2, 1.482, fala, 0.000050, 0.000125, 1, 1) )
#
#vals01.reverse()
#vals11.reverse()
#x = [val["v"]/sqrt(2) for val in vals01]
#y = [val["b"] / val["ko"] for val in vals01]
#plt.plot(x,y)
#x = [val["v"]/sqrt(2) for val in vals11]
#y = [val["b"] / val["ko"] for val in vals11]
#plt.plot(x,y)
# b01=1-math.pow((1+sqrt(2))/(1+math.pow( 4+math.pow(v,4) ,0.25) ),2)
# bee = (math.pow(b/ko,2)-math.pow(n2,2))/(n1**2 - n2**2)
