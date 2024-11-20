import math

def rotate_point(x, y, cx, cy, theta):
    # Translate point to origin
    temp_x = x - cx
    temp_y = y - cy

    # Apply rotation
    rotated_x = temp_x * math.cos(theta) - temp_y * math.sin(theta)
    rotated_y = temp_x * math.sin(theta) + temp_y * math.cos(theta)

    # Translate point back
    new_x = rotated_x + cx
    new_y = rotated_y + cy

    return new_x, new_y