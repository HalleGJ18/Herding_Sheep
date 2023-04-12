import numpy as np

# get magnitude of a given vector
def vector_magnitude(v):
    return np.linalg.norm(v)

# get the unit vector version of a given vector
def unit_vector(v):
    return v/vector_magnitude(v)

# get n closest agents
def get_n_closest(self, target, dists):
    # target is agent you are measuring from
    # dists is matrix of distances between agents
    # dists[target] gets array of other agents
    #TODO: does this need a check for dog x sheep or sheep x sheep matrix to account for same agent being 0 distance?
    pass