x = 1
y = 0.9

# if x in range(2,6):
#     print("first")
  
# if x in range(0,2):
#     print("second")

x1 = 1
width = 3

y1=1
height = 2

# if (x>=x1 and x<=x1+width) and (y>=y1 and y<=y1+height):
#     print("inside")
# else:
#     print("outside")


from shepherding.obstacle import calc_collision_in_x

collide, y_pred = calc_collision_in_x([2.0, 3.0], [1.5, 0.5], 3.0, 2.0, 7.0)
print(collide, y_pred)

collide, y_pred = calc_collision_in_x([8.0,4.0], [-1.0, -1.0], 7.0, 2.0, 5.0)
print(collide, y_pred)

collide, y_pred = calc_collision_in_x([2.0, 3.0], [-1.5, -0.5], 3.0, 2.0, 7.0)
print(collide, y_pred)


from shepherding.obstacle import calc_collision_in_y

collide, x_pred = calc_collision_in_y([1.0, 15.0], [0.25, -1.5], 3.0, 1.0, 10.0)
print(collide, x_pred)