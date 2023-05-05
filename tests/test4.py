def line_segments_intersect(seg1, seg2):
    """
    Checks if two line segments intersect.

    Parameters:
    seg1 (tuple): A tuple of two points representing the first line segment.
    seg2 (tuple): A tuple of two points representing the second line segment.

    Returns:
    bool: True if the line segments intersect, False otherwise.
    """
    x1, y1 = seg1[0]
    x2, y2 = seg1[1]
    x3, y3 = seg2[0]
    x4, y4 = seg2[1]

    # Compute the cross products
    cross_product1 = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    cross_product2 = (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)
    cross_product3 = (x4 - x1) * (y2 - y1) - (y4 - y1) * (x2 - x1)

    # Check if the line segments intersect
    if cross_product1 == 0 and cross_product2 == 0 and cross_product3 == 0:
        # Line segments are collinear, check if they overlap
        if x1 <= max(x3, x4) and x1 >= min(x3, x4) and y1 <= max(y3, y4) and y1 >= min(y3, y4):
            return True
        if x2 <= max(x3, x4) and x2 >= min(x3, x4) and y2 <= max(y3, y4) and y2 >= min(y3, y4):
            return True
    else:
        # Line segments are not collinear, check if they intersect
        if cross_product1 != 0 and cross_product2 != 0 and cross_product3 != 0:
            return True

    return False

def line_intersect_rect(line, rect):
    for side in rect:
        if line_segments_intersect(line, side):
            print(True)
    print(False)

line1 = [[2,1],[6,10]] # Yes
line2 = [[2,1],[10,6]] # Yes
line3 = [[2,1],[8,1]] # No
line4 = [[2,1],[0.5,6]] # Yes

side1 = [[1,4],[9,4]]
side2 = [[1,4],[1,8]]
side3 = [[1,8],[9,8]]
side4 = [[9,4],[9,8]]

rect = [side1, side2, side3, side4]

# print(line_segments_intersect(line3, side2))

# print(line_intersect_rect(line1, rect))
# print(line_intersect_rect(line2, rect))
# print(line_intersect_rect(line3, rect))
# print(line_intersect_rect(line4, rect))

print("1")
line_intersect_rect(line1, rect)
print("2")
line_intersect_rect(line2, rect)
print("3")
line_intersect_rect(line3, rect)
print("4")
line_intersect_rect(line4, rect)