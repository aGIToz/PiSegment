import cv2
import numpy as np

# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1

# Mouse callback function
def annotate(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_RBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(img, (x, y), 1, color, -1)

    elif event == cv2.EVENT_RBUTTONUP:
        drawing = False
        cv2.circle(img, (x, y), 1, color, -1)


def create_mask(input_path, mask_path):
    global img
    img = cv2.imread(input_path)
    img = np.where(img == 0, 1, img) # add noise
    global color
    color = (0,0,0)
    cv2.namedWindow('image',cv2.WINDOW_GUI_NORMAL) # Qt backend assumption!
    cv2.setMouseCallback('image', annotate)

    while True:
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('1'):
            color = (0,0,0) 

        if k == ord('2'):
            color = (255, 0, 0)

        if k == ord('3'):
            color = (0, 255, 0)

        if k == ord('4'):
            color = (0, 0, 255)

        if k == ord('5'):
            color = (255, 0, 255)

        if k == ord('6'):
            color = (255, 255, 0)

        if k == ord('7'):
            color = (0, 255, 255)

        if k == ord('8'):
            color = (0, 125, 255)

        if k == ord('9'):
            color = (125, 0, 255)

        # Press 's' to save the mask
        if k == ord('s'):
            condition1 = np.all(img == [0, 0, 0], axis=-1)
            condition2 = np.all(img == [255, 0, 0], axis=-1)
            condition3 = np.all(img == [0, 255, 0], axis=-1)
            condition4 = np.all(img == [0, 0, 255], axis=-1)
            condition5 = np.all(img == [255, 0, 255], axis=-1)
            condition6 = np.all(img == [255, 255, 0], axis=-1)
            condition7 = np.all(img == [0, 255, 255], axis=-1)
            condition8 = np.all(img == [0, 125, 255], axis=-1)
            condition9 = np.all(img == [125, 0, 255], axis=-1)
            final_condition = condition1 | condition2 | condition3 | condition4 | condition5 | condition6 | condition7 | condition8 | condition9
            img[~final_condition] = [255, 255, 255]

            cv2.imwrite(f'{mask_path}', img)
            print(f"Mask saved as '{mask_path}'")
            break

        # Press 'esc' to exit
        elif k == 27:
            break

    cv2.destroyAllWindows()
