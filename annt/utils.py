
import cv2

def draw_rectangle(image, p1, p2, color, alpha):
    overlay = image.copy()
    cv2.rectangle(image, p1, p2, color, -1)
    image = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0)
    return image