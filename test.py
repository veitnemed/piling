import numpy as np

R_min = 0.1
R_max = 10.0
R_delta = 0.1
R_count = 10
R_VALUES = np.linspace(R_min, R_max, R_count, endpoint = False)
print(R_VALUES)