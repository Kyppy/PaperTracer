# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:04:15 2017

@author: Kyppy Simani
"""
import cv2
import numpy as np
import time
import serial

# Bluetooth comm settings
ser = serial.Serial(
    port='COM6',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=3)

print("Connected to: " + ser.portstr)

# Variable initialising
avg = []  # color scan averaging
pos = []  # general use array to store postion data
corners = [[0, 0], [0, 0], [0, 0], [0, 0]]  # array to store corner positions
setpoint = [[0, 0]]  # setpoint location
beacon = []  # stores beacon postion
p = 0  # coordinate check flag
k = 0  # beacon chek flag
l = 0  # direction change tracking flag
margin = 35  # #Set the margin distance in pixels.Approximately 2.54cm
error = 5  # one step is approximately 3 pixels(1.91 mm).Therefore error of one step allowed
search_mode = 1
write_mode = 0

# HSV color boundaries for the 'purple' beacon
hsvLower = (119, 145, 24)
hsvUpper = (133, 255, 190)

delta_x = 0  # change in horizontal motion
delta_y = 0  # change in vertical motion

# corner pixel check flags
f1 = 0
f2 = 0
f3 = 0
f4 = 0

# color thresholds for single sweeep corners
bmin = 126  # 96
gmin = 105  # 110
rmin = 121  # 105

# pixel length based on A4 page measurements
pix_size = 0.717  # millimeters

# Appoximate nozzle bank length
NBL = 6  # value in pixels

# cropping and pixel-search sweep clearance flag
cropping_cleared = 0
cornerdet_cleared = 0
pixelsweep_cleared = 0

# //////////////////////////////////////////////////////////////////////////////

# Grab reference to the webcam
cap = cv2.VideoCapture(0)

while (True):
    # wait 3 seconds (DEBUGGING PURPOSES ONLY)
    # time.sleep(0.5)

    # Take frame from camera for processing
    ret, image = cap.read()

    # Crop out everything around white paper in the frame
    rows, columns, channels = image.shape

    # START ONE TIME CROP HERE#
    if (cropping_cleared != 1):
        # topleft corner - horizontal sweep
        for i in range(0, (rows // 2)):

            if p == 1:

                break

            else:

                for j in range(0, (columns // 2)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        tl_row_horz = pos[0][0]
                        tl_col_horz = pos[0][1]

                        break

        p = 0
        # topleft corner - vertical sweep
        for j in range(0, (columns // 2)):

            if p == 1:

                break

            else:

                for i in range(0, (rows // 2)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        tl_row_vert = pos[0][0]
                        tl_col_vert = pos[0][1]

                        break

        p = 0

        # topright corner - horizontal sweep
        for i in range(0, (rows // 2)):

            if p == 1:

                break

            else:

                for j in reversed(range((columns // 2), columns)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        tr_row_horz = pos[0][0]
                        tr_col_horz = pos[0][1]

                        break

        p = 0
        # topright corner - vertical sweep
        for j in reversed(range((columns // 2), columns)):

            if p == 1:

                break

            else:

                for i in range(0, (rows // 2)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        tr_row_vert = pos[0][0]
                        tr_col_vert = pos[0][1]

                        break

        p = 0

        # bottomleft corner - horizontal sweep
        for i in reversed(range((rows // 2), rows)):

            if p == 1:

                break

            else:

                for j in range(0, (columns // 2)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        bl_row_horz = pos[0][0]
                        bl_col_horz = pos[0][1]

                        break

        p = 0
        # bottomleft corner - vertical sweep
        for j in range(0, (columns // 2)):

            if p == 1:

                break

            else:

                for i in reversed(range((rows // 2), rows)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        bl_row_vert = pos[0][0]
                        bl_col_vert = pos[0][1]

                        break

        p = 0

        # bottomright corner - horizontal sweep
        for i in reversed(range((rows // 2), rows)):

            if p == 1:

                break

            else:

                for j in reversed(range((columns // 2), columns)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        br_row_horz = pos[0][0]
                        br_col_horz = pos[0][1]

                        break

        p = 0
        # bottomright corner - vertical sweep
        for j in reversed(range((columns // 2), columns)):

            if p == 1:

                break

            else:

                for i in reversed(range((rows // 2), rows)):

                    B = image.item(i, j, 0)
                    G = image.item(i, j, 1)
                    R = image.item(i, j, 2)
                    avg = ((B + G + R) // 2)

                    if B >= bmin and G >= gmin and R >= rmin:
                        pos = [[i, j]]
                        p = 1
                        # print(pos)

                        br_row_vert = pos[0][0]
                        br_col_vert = pos[0][1]

                        break

        p = 0
        # crop pixel sweeping end

        # //////////////////////////////////////////////////////////////////////////////
        # Determine cropping corners
        y1 = min(tl_row_horz, bl_row_horz)
        y2 = max(bl_row_horz, br_row_horz)

        x1 = min(tl_col_vert, bl_col_vert)
        x2 = max(tr_col_vert, br_col_vert)

        crop_row = (y2 - y1)
        crop_column = (x2 - x1)

        row_mid = y1 + (crop_row // 2)  # cropped page image vertical midpoint
        col_mid = x1 + (crop_column // 2)  # cropped page image horizontal midpoint

        page_height = (crop_row * pix_size)
        page_width = (crop_column * pix_size)

        # print("Page dimensions are approximately",page_width,"mm x",page_height,"mm")
        print("Page dimensions are approximately %.2f mm x %.2f mm " % (page_width, page_height))

        cropping_cleared = 1

    # END ONE TIME CROP HERE#

    crop = image[y1:y2, (x1 + 0):(x2 - 0)]  # apply cropping points to webcam image

    # create black background of size 480 by 640.
    # transpose cropped image onto black background.
    # ensures consistent sized frames sent for corner detecting
    blackground = np.zeros((480, 640, 3), np.uint8)
    blackground[y1:y2, (x1 + 0):(x2 - 0)] = crop

    # //////////////////////////////////////////////////////////////////////////////
    # Apply corner detection method to cropped camera image frame
    pic = blackground
    img = pic

    # START OF ONE-TIME CROPPED IMAGE CORNER DETECTION#

    if (cornerdet_cleared != 1):
        gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        cornerdet_cleared = 1

    # END OF ONE-TIME CROPPED IMAGE CORNER DETECTION#

    img[dst > 0.01 * dst.max()] = [0, 0, 255]
    rows, columns, channels = img.shape

    # //////////////////////////////////////////////////////////////////////////////
    # Corner Detection

    # Scan each pixel of the corner detection processed frame row by row
    # If the pixel is 'pure' red then a corner has been detected.
    # Raise a flag once the bottomright corner has been accounted for.
    # This code (V2) has been changed so that page tilt is no longer a concern for
    # corner detection accuracy.

    # START OF ONE-TIME PIXEL SWEEP#

    for i in range(y1, row_mid):  # topleft corner

        if p == 1:

            break

        else:

            for j in range(x1, col_mid):

                pix = img.item(i, j, 2)

                if pix == 255:
                    pos = [[j, i]]
                    corners[0][0] = pos[0][0]
                    corners[0][1] = pos[0][1]
                    f1 = 1
                    p = 1
                    break

    p = 0

    for i in range(y1, row_mid):  # topright corner

        if p == 1:

            break

        else:

            for j in reversed(range(col_mid, x2)):

                pix = img.item(i, j, 2)

                if pix == 255:
                    pos = [[j, i]]
                    corners[1][0] = pos[0][0]
                    corners[1][1] = pos[0][1]
                    f2 = 1
                    p = 1
                    break

    p = 0

    for i in reversed(range(row_mid, y2)):  # bottomleft corner

        if p == 1:

            break

        else:

            for j in range(x1, col_mid):

                pix = img.item(i, j, 2)

                if pix == 255:
                    pos = [[j, i]]
                    corners[2][0] = pos[0][0]
                    corners[2][1] = pos[0][1]
                    f3 = 1
                    p = 1
                    break

    p = 0

    for i in reversed(range(row_mid, y2)):  # bottomright corner

        if p == 1:

            break

        else:

            for j in reversed(range(col_mid, x2)):

                pix = img.item(i, j, 2)

                if pix == 255:
                    pos = [[j, i]]
                    corners[3][0] = pos[0][0]
                    corners[3][1] = pos[0][1]
                    f4 = 1
                    p = 1
                    break

    # Confirm successful corner sweep
    if f1 and f2 and f3 and f4 == 1:
        print("Complete Corner Search")

    else:
        print("Incomplete Corner Search")

    pixelsweep_cleared = 1
    # END OF ONE-TIME PIXEL SWEEP#

    # //////////////////////////////////////////////////////////////////////////////
    # Calculate contour and centroid of the beacon

    # construct mask for beacon
    maskground = cv2.cvtColor(blackground, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(maskground, hsvLower, hsvUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the center of the beacon
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask.
        # this is used to compute the circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius < 20:
            # draw the circle and centroid
            cv2.circle(pic, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(pic, center, 1, (0, 0, 255), -1)
    # //////////////////////////////////////////////////////////////////////////////
    # Navigation settings

    # Setpoint initialisations
    setpoint_horz = corners[0][0] + margin
    setpoint_vert = corners[0][1] + margin

    # Define margin corners for outline
    tl_setpoint_horz = corners[0][0] + margin
    tl_setpoint_vert = corners[0][1] + margin

    tr_setpoint_horz = corners[1][0] - margin
    tr_setpoint_vert = corners[1][1] + margin

    bl_setpoint_horz = corners[2][0] + margin
    bl_setpoint_vert = corners[2][1] - margin

    br_setpoint_horz = corners[3][0] - margin
    br_setpoint_vert = corners[3][1] - margin

    ####SETPOINT TESTING CODE BLOCK####
    # setpoint_horz = corners[0][0] + (( max(corners[1][0],corners[3][0]) - min(corners[0][0],corners[2][0]) )) // 2
    # setpoint_vert = corners[0][1] + (( max(corners[2][1],corners[3][1]) - min(corners[0][1],corners[1][1]) )) // 2
    ##############################

    setpoint[0][0] = setpoint_horz  # x co-ord
    setpoint[0][1] = setpoint_vert  # y co-ord

    # Error band definitions
    upper_bar = setpoint[0][1] - error
    lower_bar = setpoint[0][1] + error

    left_bar = setpoint[0][0] - error
    right_bar = setpoint[0][0] + error

    # Printing page border limits
    left_edge = min(corners[0][0], corners[2][0]) + margin
    right_edge = max(corners[1][0], corners[3][0]) - margin
    top_edge = min(corners[0][1], corners[1][1]) + margin
    bottom_edge = max(corners[2][1], corners[3][1]) - margin

    # Display setpoint position
    cv2.circle(pic, (int(setpoint_horz), int(setpoint_vert)), 3, (0, 0, 255), -1)

    # setpoint lies within error-band plus/minus error pixels
    if len(cnts) > 0:

        if ((setpoint_horz - error) < center[0] < (setpoint_horz + error)) and (
                (setpoint_horz - error) < center[1] < (setpoint_horz + error)):
            print("Beacon In Position")
            ser.write(b'5')

    # //////////////////////////////////////////////////////////////////////////////
    # Determine beacon position quadrant and calulate distance from setpoint

    corner_row = (max(corners[2][1], corners[3][1]) - min(corners[0][1], corners[1][1]))
    corner_column = (max(corners[1][0], corners[3][0]) - min(corners[0][0], corners[2][0]))

    columns_mid = (min(corners[0][0], corners[2][0]) + (corner_column // 2))
    rows_mid = (min(corners[0][1], corners[1][1]) + (corner_row // 2))

    if len(cnts) > 0:

        if (center[1] < rows_mid) and (center[0] < columns_mid):

            print("Beacon Quadrant:Topleft")
            print("Position", center[0], center[1])


        elif (center[1] < rows_mid) and (center[0] > columns_mid):

            print("Beacon Quadrant:Topright")
            print("Position", center[0], center[1])


        elif (center[1] > rows_mid) and (center[0] < columns_mid):

            print("Beacon Quadrant:Bottomleft")
            print("Position", center[0], center[1])


        elif (center[1] > rows_mid) and (center[0] > columns_mid):

            print("Beacon Quadrant:Bottomright")
            print("Position", center[0], center[1])

    else:
        print("Beacon Not Detected")
        ser.write(b'5')

    if len(cnts) > 0:
        # draw line from beacon centre to setpoint
        cv2.line(pic, (center[0], center[1]), (int(setpoint_horz), int(setpoint_vert)), (0, 0, 255), 2)

        # draw print margin outlines
        cv2.line(pic, (int(tl_setpoint_horz), int(tl_setpoint_vert)), (int(tr_setpoint_horz), int(tr_setpoint_vert)),
                 (0, 0, 255), 1)
        cv2.line(pic, (int(tl_setpoint_horz), int(tl_setpoint_vert)), (int(bl_setpoint_horz), int(bl_setpoint_vert)),
                 (0, 0, 255), 1)

        cv2.line(pic, (int(tr_setpoint_horz), int(tr_setpoint_vert)), (int(br_setpoint_horz), int(br_setpoint_vert)),
                 (0, 0, 255), 1)
        cv2.line(pic, (int(br_setpoint_horz), int(br_setpoint_vert)), (int(bl_setpoint_horz), int(bl_setpoint_vert)),
                 (0, 0, 255), 1)

        # calculate remaining distance from centre to distance in mm
        # x_dist and y_dist results are in pixels
        x_dist_px = abs(setpoint_horz - center[0])
        y_dist_px = abs(setpoint_vert - center[1])

        x_dist_mm = (x_dist_px * pix_size)
        y_dist_mm = (y_dist_px * pix_size)

        print("Distance from setpoint in x coordinate is %.2f mm" % (x_dist_mm))
        print("Distnace from setpoint in y coordinate is %.2f mm" % (y_dist_mm))

    # //////////////////////////////////////////////////////////////////////////////
    # Hunt for the setpoint

    if (len(cnts) > 0) and search_mode == 1:

        # if too far left,move towards the right edge
        if (center[0] < (setpoint_horz - error)):

            ser.write(b'1')

            # if too far right,move towards the left egde
        elif (center[0] > (setpoint_horz + error)):  # if

            ser.write(b'2')

        # if too high up,move towards the bottom edge
        elif (center[1] < (setpoint_vert - error)):

            ser.write(b'4')

        # if too far low,move towards the top edge
        elif (center[1] > (setpoint_vert + error)):

            ser.write(b'3')

        # stop when its within the error band of the setpoint
        elif ((setpoint_horz - error) <= center[0] <= (setpoint_horz + error)) and (
                (setpoint_vert - error) <= center[1] <= (setpoint_vert + error)):

            ser.write(b'5')
            search_mode = 0
            write_mode = 1

        else:

            ser.write(b'5')
        # //////////////////////////////////////////////////////////////////////////////
    # Print out text

    if (len(cnts) > 0) and write_mode == 1:

        # BEGIN 'L' sequence
        # downstroke
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'4')
            ser.write(b'5')
            # right stroke
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[0]  # store x coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
            # space
        for steps in range(0, 11):
            ser.write(b'5')  # pause
            past = center[0]  # store x coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')

        # BEGIN 'E' sequence
        # upstroke
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'3')
            ser.write(b'5')
        # top stroke to right
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[0]  # store x coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
        # return from right-to-left
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'2')
            ser.write(b'5')
        # downstroke
        for steps in range(0, 8):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'4')
            ser.write(b'5')
            # mid stroke to right
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
        # return from right to left
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'2')
            ser.write(b'5')
        # downstroke
        for steps in range(0, 8):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'4')
            ser.write(b'5')
            # bottom stroke to right
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
            # space
        for steps in range(0, 11):
            ser.write(b'5')  # pause
            past = center[0]  # store x coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')

            # BEGIN 'F' sequence
        # upstroke
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'3')
            ser.write(b'5')
            # top stroke to right
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
            # return from right to left
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'2')
            ser.write(b'5')
            # downstroke
        for steps in range(0, 8):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'4')
            ser.write(b'5')
            # mid stroke to right
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
            # return from right to left
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'2')
            ser.write(b'5')
            # downstroke
        for steps in range(0, 8):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'4')
            ser.write(b'5')
            # space
        for steps in range(0, 26):
            ser.write(b'5')  # pause
            past = center[0]  # store x coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')

            # BEGIN 'T' sequence
        # upstroke
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'3')
            ser.write(b'5')
            # top stroke from mid to left
        for steps in range(0, 10):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'2')
            ser.write(b'5')
        # return to mid from left
        for steps in range(0, 10):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'1')
            ser.write(b'5')
            # top stroke from mid to right
        for steps in range(0, 10):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'1')
            ser.write(b'5')
            # return to mid from right
        for steps in range(0, 10):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'2')
            ser.write(b'5')
        # downstroke
        for steps in range(0, 16):
            ser.write(b'5')  # pause
            past = center[1]  # store y coordinate before move
            ser.write(b'6')  # ink ejection
            time.sleep(0.015)  # wait for ejection to finish
            ser.write(b'4')
            ser.write(b'5')
        # ==============================================================================
        #         while(int(center[1]) <= past): #confirm complete step i.e no slip.Otherwise keep stepping
        #             #construct mask for beacon
        #             maskground = cv2.cvtColor(blackground,cv2.COLOR_BGR2HSV)
        #             mask = cv2.inRange(maskground, hsvLower,hsvUpper)
        #             mask = cv2.erode(mask,None,iterations = 2)
        #             mask = cv2.dilate(mask,None,iterations = 2)
        #
        #             #find contours in the mask and initialize the center of the beacon
        #             cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        #             center = None
        #
        #             #proceed if at least one contour was found
        #             #if len(cnts) > 0:
        #                 #find the largest contour in the mask.
        #                 #this is used to compute the circle and centroid
        #             c = max(cnts, key=cv2.contourArea)
        #             ((x,y), radius) = cv2.minEnclosingCircle(c)
        #             M = cv2.moments(c)
        #             center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #             ser.write(b'4')
        #             ser.write(b'5')
        #
        # ==============================================================================
        write_mode = 0
        ser.write(b'5')
    # //////////////////////////////////////////////////////////////////////////////
    # Reinitialize flags for next loop
    p = 0
    k = 0
    f = 0
    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0

    print("")
    # //////////////////////////////////////////////////////////////////////////////
    # Break from tracking loop when 'q' is pressed
    cv2.imshow('frame', pic)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close
print("Page dimensions are approximately %.2f mm x %.2f mm " % (page_width, page_height))







