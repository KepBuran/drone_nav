# def control_point(x1, y1, x2, y2, fraction):
#     x_distance = x2 - x1
#     y_distance = y2 - y1
#     cx = x1 + fraction * (x2 - x1)
#     cy = y1 + fraction * (y2 - y1
#     offset_x_max = x_distance // 15
#     offset_y_max = y_distance // 1
#     offset_x = random.randint(-offset_x_max, offset_x_max)
#     offset_y = random.randint(-offset_y_max, offset_y_max)
#     return int(cx + offset_x), int(cy + offset_y)

# cx1, cy1 = control_point(x1, y1, x2, y2, 1/3)
# cx2, cy2 = control_point(x1, y1, x2, y2, 2/3)

# def bezier(t, p0, p1, p2, p3):
#     return (1-t)**3 * p0 + 3 * (1-t)**2 * t * p1 + 3 * (1-t) * t**2 * p2 + t**3 * p

# distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2
                     
# # Populate growth_grid with a curvy line using the Bezier curve
# for i in range(math.floor(distance) + 1):   
#     t = i / 10
#     bx = int(bezier(t, x1, cx1, cx2, x2))
#     by = int(bezier(t, y1, cy1, cy2, y2))
#     print(bx, by)
    
#     for w in range(-width, width + 1):
#         if 0 <= bx + w < grid_width and 0 <= by + w < grid_height:
#             growth_grid[by + w][bx + w] += growth

base = 53440227.515






arr=[
    108449108.647,
53311415.415,
129538017.50

]

# Convert arr values to percentages relative to base
percentages = [(value / base) * 100 for value in arr]

print(percentages)