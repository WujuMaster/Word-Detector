import cv2
import numpy as np


def removeLine(image, thresh):
    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
        
    # Remove vertical
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

def findCorners(bound):
    # x of left, y of top
    top_left = [bound[3][0],bound[0][1]]
    # x of right, y of bottom
    bottom_right = [bound[1][0],bound[2][1]]
    return [top_left, bottom_right]

def detectWords(im_pil):
    img = np.asarray(im_pil)
    img_og = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    se = cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
    bg = cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
    img = cv2.divide(img, bg, scale=255)

    thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    removeLine(img, thresh)

    blur = cv2.GaussianBlur(img, (3,3), 0)
    _, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area of the rectangle to be detected.
    # A smaller value like (10, 10) will detect each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 10))
    # Applying dilation on the threshold image
    th3 = cv2.dilate(th3, rect_kernel, iterations = 1)

    # cv2.imshow('After dilation', cv2.resize(th3, (600, round(600*th3.shape[0]/th3.shape[1]))))
    # cv2.waitKey(0)

    bndingBx = []
    # reassign contours to the filled in image
    contours, heirar = cv2.findContours(th3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # find the rectangle around each contour
    for num in range(0,len(contours)):
        # make sure contour is for letter and not cavity
        if(heirar[0][num][3] == -1):
            left = tuple(contours[num][contours[num][:,:,0].argmin()][0])
            right = tuple(contours[num][contours[num][:,:,0].argmax()][0])
            top = tuple(contours[num][contours[num][:,:,1].argmin()][0])
            bottom = tuple(contours[num][contours[num][:,:,1].argmax()][0])
            bndingBx.append([top,right,bottom,left])

    corners = []
    for bx in bndingBx:
        corners.append(findCorners(bx))

    # draw the boxes
    for top_left, bottom_right in corners:
        cv2.rectangle(img_og, (top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]), 
                                (0, 255, 0), 
                                2)

    return img_og


