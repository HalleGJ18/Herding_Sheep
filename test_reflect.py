def reflect_vector(vector, normal):
    dot_product = 2 * (vector[0] * normal[0] + vector[1] * normal[1])
    reflected_vector = [vector[0] - dot_product * normal[0], vector[1] - dot_product * normal[1]]
    return reflected_vector

original_vector = [3, 4]
surface_normal = [1, 0]  # Assuming the surface normal is along the x-axis

reflected_vector = reflect_vector(original_vector, surface_normal)
print(reflected_vector)  # Output: [3, -4]

original_vector = [3, -4]
surface_normal = [-1, 0]  # Assuming the surface normal is along the x-axis

reflected_vector = reflect_vector(original_vector, surface_normal)
print(reflected_vector)  # Output: [3, -4]


original_vector = [3, -4]
surface_normal = [0, 1]  # Assuming the surface normal is along the x-axis

reflected_vector = reflect_vector(original_vector, surface_normal)
print(reflected_vector)  # Output: [3, -4]



original_vector = [3, 4]
surface_normal = [0, -1]  # Assuming the surface normal is along the x-axis

reflected_vector = reflect_vector(original_vector, surface_normal)
print(reflected_vector)  # Output: [3, -4]

v=[-1, -1]
n=[1,0]
reflected_vector = reflect_vector(v, n)
print(reflected_vector)