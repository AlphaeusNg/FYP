import cv2

def display_image_with_coordinates(image_path: str = r"uploads\annotated_Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma-03.png", window_width: int = 800, window_height: int = 600):
    """
    Display an image with the current mouse coordinates shown at the bottom-right corner of the window.

    Args:
        image_path (str): Path to the image file.
        window_width (int): Width of the display window.
        window_height (int): Height of the display window.
    """
    # Function to handle mouse events
    def mouse_event(event, x, y, flags, param):
        nonlocal clicks, coordinates
        if event == cv2.EVENT_LBUTTONDOWN:
            clicks += 1
            coordinates.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Image', image)
            if clicks == 2:
                x1, y1 = coordinates[0]
                x2, y2 = coordinates[1]
                print(f"Coordinates: ({x1}, {y1}), ({x2}, {y1}), ({x1}, {y2}), ({x2}, {y2}) | {x1,y1,x2,y2}")
                # Reset clicks counter and coordinates list
                clicks = 0
                coordinates.clear()

    # Read an image
    image = cv2.imread(image_path)
    clicks = 0
    coordinates = []

    # Set window size
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', window_width, window_height)

    # Display the image
    cv2.imshow('Image', image)

    # Set mouse callback function for window
    cv2.setMouseCallback('Image', mouse_event)

    # Wait indefinitely for any key to be pressed
    cv2.waitKey(0)

if __name__ == "__main__":
    display_image_with_coordinates()
