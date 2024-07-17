import numpy as np
import cv2

def generate_marker(id, size=400):
    # Create a black square of the given size
    marker = np.zeros((size, size), dtype=np.uint8)
    
    # Calculate the cell size for the grid
    cell_size = size // 5

    # Set the pattern for the marker
    pattern = [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, id % 2, 0, 1],  # Central cell changes based on ID
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ]

    # Draw the pattern on the marker
    for row in range(5):
        for col in range(5):
            if pattern[row][col] == 1:
                cv2.rectangle(marker, (col*cell_size, row*cell_size), 
                              ((col+1)*cell_size, (row+1)*cell_size), 255, -1)

    return marker

# Generate a marker with ID 1
marker = generate_marker(id=1)

# Save the marker as an image
cv2.imwrite('custom_marker.png', marker)

# Display the marker
cv2.imshow('Marker', marker)
cv2.waitKey(0)
cv2.destroyAllWindows()
