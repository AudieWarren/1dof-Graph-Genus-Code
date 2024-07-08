point =  [[0, 4847, 0, 2886, 0, 6257, 1662, 0, 1662, 1662, 7412, 2638, 3718, 1310, 7867, 7412, 1310, 1310, 7412, 2638], [0, 0, 3596, 667, 9178, 0, 1022, 667, 667, 4751, 667, 3312, 667, 2795, -700, 635, 1022, -700, -700, 635]]
weights = []
for i in range(len(point[0])):
    weights.append(point[0][i]+point[1][i])
    
print(f"weights are {weights}")
if len(weights) != len(set(weights)):
    print("There are non-distinct weights")
    
weightsdiffs = []
for i in range(len(weights)):
  for j in range(i+1,len(weights)):
    weightsdiffs.append(weights[i]-weights[j])
  # print(f"Weights are {weights}")
    # print(f"Weight differences are {weightsdiffs}")
    # print(f"weight differences len is {len(weightsdiffs)}")
    # print(f"weightdifferences set is {len(set(weightsdiffs))}")
  if len(weightsdiffs) != len(set(weightsdiffs)):
    print(f"there are repeated weight differences")
print(f"Weight differences are {weightsdiffs}")
print(f"weight differences len is {len(weightsdiffs)}")
print(f"weightdifferences set is {len(set(weightsdiffs))}")