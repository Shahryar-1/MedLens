def print_pixel_info(frame, x, y):
    """
    Print the BGR values of a pixel.

    Parameters:
        frame : numpy.ndarray
            Image captured from OpenCV.

        x : int
            X coordinate (column).

        y : int
            Y coordinate (row).
    """

    blue = frame[y, x][0]
    green = frame[y, x][1]
    red = frame[y, x][2]

    print("\n========== PIXEL INFORMATION ==========")
    print(f"Position : ({x}, {y})")
    print(f"Blue     : {blue}")
    print(f"Green    : {green}")
    print(f"Red      : {red}")
    print("=======================================\n")