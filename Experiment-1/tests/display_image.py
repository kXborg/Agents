import cv2
import numpy as np

# Load an image from file
# Make sure 'image.jpg' is in the same directory as the script
# or provide a full path
img = cv2.imread('image.jpg')

# Check if image was loaded successfully
if img is None:
    print('Error: Could not load image. Please check the path and filename.')
    else:
        # Display the image in a window
            cv2.imshow('Display Image', img)

                # Wait for a key press indefinitely (0 means wait forever)
                    # until any key is pressed
                        cv2.waitKey(0)

                            # Destroy all OpenCV windows
                                cv2.destroyAllWindows()