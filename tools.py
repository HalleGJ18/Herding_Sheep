import numpy as np

# get magnitude of a given vector
def vector_magnitude(v):
    return norm(v)

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


def line_rect_intersect(line, rect):
    """
    Checks if a line intersects with a rectangle.

    Parameters:
    line (tuple): A tuple of two points representing the line.
    rect (tuple): A tuple of two floats representing the bottom-left corner of the rectangle, and two floats representing the width and height of the rectangle.

    Returns:
    bool: True if the line intersects with the rectangle, False otherwise.
    """
    x1, y1 = line[0]
    x2, y2 = line[1]
    corner, width, height = rect
    x_min, y_min = corner

    # Calculate the values of p and q for the line
    dx = x2 - x1
    dy = y2 - y1
    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_min + width - x1, y1 - y_min, y_min + height - y1]

    # Initialize the values of u1 and u2 to be 0 and 1, respectively
    u1 = 0
    u2 = 1

    # Clip the line against each edge of the rectangle
    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                # Line is parallel to the edge and outside the rectangle
                return False
        else:
            r = q[i] / p[i]
            if p[i] < 0:
                if r > u2:
                    # Line is outside the rectangle
                    return False
                elif r > u1:
                    u1 = r
            elif p[i] > 0:
                if r < u1:
                    # Line is outside the rectangle
                    return False
                elif r < u2:
                    u2 = r

    # Check if the clipped line intersects the rectangle
    if u1 > 0 or u2 < 1:
        x1_clip = x1 + u1 * dx
        y1_clip = y1 + u1 * dy
        x2_clip = x1 + u2 * dx
        y2_clip = y1 + u2 * dy
        if (x_min <= x1_clip <= x_min + width or x_min <= x2_clip <= x_min + width) and \
                (y_min <= y1_clip <= y_min + height or y_min <= y2_clip <= y_min + height):
            return True

    return False