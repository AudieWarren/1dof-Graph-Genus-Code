import random

size = 1000
smallsize = 100

def arb():
  return random.randint(1,size)

def smallarb():
  return random.randint(-smallsize,smallsize)

def arbsp():
  return random.randint(1,500)