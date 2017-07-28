'''
Created on 28 July 2017
MapReduce job to calculate mean and variance
  of a bunch of numbers

@autor: resema
'''

import sys
from numpy import mat, mean, power

'''
generator returns an iterator known as generator
  loops step by step until yield and returns 
    in every function call the next value from yield
  all local state is retaied during suspention
'''
def read_input(file):
  for line in file:
    yield line.rstrip()   # used when defining a generator function

input = read_input(sys.stdin)
input = [float(line) for line in input]
numInputs = len(input)
input = mat(input)
sqInput = power(input, 2)

print '%d\t%f\t%d' % (numInputs, mean(input), mean(sqInput))
print >> sys.stderr, "report: still alive"








































