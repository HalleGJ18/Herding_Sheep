import numpy as np

# get magnitude of a given vector
def vector_magnitude(v):
    return np.linalg.norm(v)

# get the unit vector version of a given vector
def unit_vector(v):
    return v/vector_magnitude(v)