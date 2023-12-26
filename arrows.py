def up_arrow():
    center_x = (5 + 45) // 2
    center_y = (5 + 45) // 2
    
    # Coordinates for the arrowhead
    arrowhead_coords = [
        (center_x, center_y - 10),  # Top point of the arrowhead
        (center_x - 5, center_y),  # Left base of the arrowhead
        (center_x + 5, center_y)   # Right base of the arrowhead
    ]
    
    # Coordinates for the tail of the arrow
    tail_start = (center_x, center_y)
    tail_end = (center_x, center_y + 10)
    return arrowhead_coords, tail_start, tail_end
    

def down_arrow():
    # Coordinates for the center of the oval
    center_x = (5 + 45) // 2
    center_y = (5 + 45) // 2
    
    # Coordinates for the downward arrowhead
    arrowhead_coords = [
        (center_x, center_y + 10),  # Bottom point of the arrowhead
        (center_x - 5, center_y),   # Top left of the arrowhead
        (center_x + 5, center_y)    # Top right of the arrowhead
    ]
    
    # Coordinates for the tail of the arrow
    tail_start = (center_x, center_y)
    tail_end = (center_x, center_y - 10)
    return arrowhead_coords, tail_start, tail_end
    
def left_arrow():
    # Coordinates for the center of the oval
    center_x = (5 + 45) // 2
    center_y = (5 + 45) // 2
    
    # Coordinates for the left arrowhead
    arrowhead_coords = [
        (center_x - 10, center_y),  # Left point of the arrowhead
        (center_x, center_y - 5),   # Top right of the arrowhead
        (center_x, center_y + 5)    # Bottom right of the arrowhead
    ]
    
    # Coordinates for the tail of the arrow
    tail_start = (center_x, center_y)
    tail_end = (center_x + 10, center_y)
    return arrowhead_coords, tail_start, tail_end
    
def right_arrow():
    # Center of the oval
    center_x = (5 + 45) // 2
    center_y = (5 + 45) // 2
    
    # Right arrowhead coordinates
    arrowhead_coords = [
        (center_x + 10, center_y),  # Right point of the arrowhead
        (center_x, center_y - 5),   # Top left of the arrowhead
        (center_x, center_y + 5)    # Bottom left of the arrowhead
    ]
    
    # Tail coordinates
    tail_start = (center_x, center_y)
    tail_end = (center_x - 10, center_y)
    return arrowhead_coords, tail_start, tail_end
