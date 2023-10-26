
import cv2

bbox = []
drawing = False

def annotation_window(img):
    """
    Draw a rectangle on an image
    """

    # mouse callback function
    def draw_rectangle(event, x, y, flags, param):

        global bbox, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            bbox = [(x, y)]
            drawing = True

        elif event == cv2.EVENT_LBUTTONUP:
            bbox.append((x, y))
            drawing = False

            # draw a rectangle around the region of interest
            p1, p2 = bbox
            cv2.rectangle(img, p1, p2, color=(0, 255, 0),thickness=1)
            cv2.imshow('image', img)

            # for bbox find upper left and bottom right points
            p1x, p1y = p1
            p2x, p2y = p2

            lx = min(p1x, p2x)
            ty = min(p1y, p2y)
            rx = max(p1x, p2x)
            by = max(p1y, p2y)

            # add bbox to list if both points are different
            if (lx, ty) != (rx, by):
                bbox = [lx, ty, rx, by]

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)

    while True:
        if not drawing:
            cv2.imshow('image', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            break

    cv2.destroyAllWindows()

    return bbox