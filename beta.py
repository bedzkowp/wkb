#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import linspace as linspace
from math import sqrt as sqrt
import math
import numpy as np

def przypadek(NA, g, n1, l, core_d, clad_d, m, p):

  def n(r):
    if r >=0 and r <= a:
      return n1 * sqrt(1 - 2 * delta * ((r /a)**g))
    else:
      return n1 * sqrt(1 - 2 * delta)
  
  def f(r):
    val = (ko**2) * (n(r)**2) - (b**2) - m**2 / (r**2)
    #val = (ko**2) * (n(r)**2) - (b**2) - 1 / (r**2)
    try:
      val = sqrt(val)
    except:
      val = 0
    return val
  
  core_r = core_d / 2
  clad_r = clad_d / 2
  a = core_r
  ko = (2 * math.pi) / l 
  
  v = (2 * math.pi * a * NA)/l
  delta = (NA**2) / (2 * (n1**2))
  
  
  n2 = n(1)

  print(n1)
  print(n2)
  
  B = np.linspace(n2*ko, n1*ko, 500)
  
  r = np.arange(0.0, clad_r, 1e-7)
  y = [ n(x) for x in r ]
  
  N = 10000
  li = np.linspace(0, clad_r, 10000)[1:]
  
  A = []
  i = 0
  for beta in B:
    b = beta
    fx = [f(x) for x in li]
    area = np.sum(fx)*(clad_r)/9999
    A.append(area)
    i+=1
  
  areadiff = [ abs(p*math.pi - x) for x in A ]
  ldiff = min(areadiff)
  
  index = areadiff.index(ldiff)
  print(ko*n1, B[index], ko*n2)
  if not (ko*n1 > B[index] > ko*n2):
    print("bad b")
  return {"area": A[index], "areadiff": areadiff[index], "b": B[index], "v": v, "ko": ko, "l": l}
  #print("area: {}  areadiff: {}, B: {}".format(A[index], areadiff[index], B[index]))
  

  #NA = 0.2
  #g=2
  #n1 = 1.482
  #l = 1550e-9
  #core_d = 0.000050

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
plt.show() 
# b01=1-math.pow((1+sqrt(2))/(1+math.pow( 4+math.pow(v,4) ,0.25) ),2)
# bee = (math.pow(b/ko,2)-math.pow(n2,2))/(n1**2 - n2**2)
