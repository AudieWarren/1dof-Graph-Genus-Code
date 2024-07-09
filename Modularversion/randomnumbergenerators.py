import random

size = 100000
smallsize = 100
spsize = 3000

def arb():
  return random.randint(1,size)

def smallarb():
  return random.randint(-smallsize,smallsize)

def arbsp():
  return random.randint(1,spsize)