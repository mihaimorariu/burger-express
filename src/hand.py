import cv2
import math
import numpy


class HandTracking:
    def __init__(self, threshold):
        HandTracking.hsv_min = (20, 70, 70)
        HandTracking.hsv_max = (30, 255, 255)
#        HandTracking.ycc_min = (0, 140, 90)
#        HandTracking.ycc_max = (255, 210, 130)
        HandTracking.hand_area_threshold = threshold
        HandTracking.capture = cv2.VideoCapture(0)

    # skin_image consists of the drawn convex hull (including polygon lines). hull4defects contains the hull in a different dataformat to be able to determine the defects.
    def ComputeHandPosition(self, skin_image, hand_contour, hull4defects):
        numpy_skin_image = numpy.asarray(skin_image[:, :])
        white_pixels = numpy.argwhere(numpy_skin_image > 0)
        number_of_white_pixels = len(white_pixels)
        sum_of_white_pixels = numpy.sum(white_pixels, axis=0)

        if number_of_white_pixels < HandTracking.hand_area_threshold:
            new_cursor_pos = None
        else:
            # Calculate the mean of the summed pixels to determine the center of the hand (and consecutively the cursor position).
            new_cursor_pos = (
                sum_of_white_pixels[1] / number_of_white_pixels, sum_of_white_pixels[0] / number_of_white_pixels)
            # Scale the cursor position to the screen resolution.
            image_size = cv.GetSize(skin_image)
            new_cursor_pos = (
                (2000/image_size[0])*new_cursor_pos[0], (1500/image_size[1])*new_cursor_pos[1])

        # Determine hull defects for the convex hull of the detected hand.
        if hand_contour:
            defects = cv.ConvexityDefects(
                hand_contour, hull4defects, cv.CreateMemStorage())
            defects_count = len(defects)

            if defects_count >= 5:
                hand_state = 0
            else:
                hand_state = 1
        else:
            # The state of the hand is set to "open" (0 is open, 1 is closed).
            hand_state = 0

        return new_cursor_pos, hand_state

    def DetectHandSkin(self, query_image):
        image_size = cv.GetSize(query_image)
        cv.Smooth(query_image, query_image, cv.CV_GAUSSIAN, 3, 3)

        query_image_hsv = cv.CreateImage(image_size, 8, 3)
        skin = cv.CreateImage(image_size, 8, 1)
        cv.CvtColor(query_image, query_image_hsv, cv.CV_BGR2HSV)

        #cv.InRangeS(query_image_hsv, (0, 30, 60), (30, 150, 255), skin)
        #cv.Threshold(skin, skin, 50, 255, cv.CV_THRESH_BINARY)
        cv.InRangeS(query_image_hsv, HandTracking.hsv_min,
                    HandTracking.hsv_max, skin)
        cv.Threshold(skin, skin, 50, 255, cv.CV_THRESH_BINARY)
        cv.Erode(skin, skin)

        contours = cv.FindContours(skin, cv.CreateMemStorage(
        ), cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)
        hand_contour = None
        max_area = 0

        # Loop over all possible contours until you find the contour with the largest surface area.
        while contours:
            current_area = math.fabs(cv.ContourArea(contours))
            if current_area > HandTracking.hand_area_threshold and current_area > max_area:
                max_area = current_area
                hand_contour = contours

            contours = contours.h_next()

        # Write convex hull polygon to dark background. Use it in ComputeHandPosition to determine center of the hand.
        if hand_contour:
            cv.Zero(skin)
            hand_contour = cv.ApproxPoly(
                hand_contour, cv.CreateMemStorage(), cv.CV_POLY_APPROX_DP, 3, 1)
            hull = cv.ConvexHull2(
                hand_contour, cv.CreateMemStorage(), cv.CV_CLOCKWISE, 1)
            cv.DrawContours(skin, hull, cv.RGB(255, 255, 255),
                            cv.RGB(255, 255, 255), 1, -1)
            hull4defects = cv.ConvexHull2(
                hand_contour, cv.CreateMemStorage(), cv.CV_CLOCKWISE, 0)
            #cv.DrawContours(skin, hull, cv.RGB(255, 0, 0), cv.RGB(255, 255, 255), 1, 2)

            cv.DrawContours(query_image, hull, cv.RGB(
                255, 255, 255), cv.RGB(255, 255, 255), 1, 2)
            cv.DrawContours(query_image, hand_contour, cv.RGB(
                0, 0, 255), cv.RGB(0, 0, 255), 1, 2)
        else:
            cv.Zero(skin)
            hand_contour = False
            hull4defects = False

        temp_image = cv.CreateImage((400, 300), 8, 3)
        cv.Resize(query_image, temp_image)
        cv.ShowImage("Camera Output", temp_image)
        cv.WaitKey(1)

        del contours

        return skin, hand_contour, hull4defects

    def GetHandPosition(self):
        current_frame = cv.QueryFrame(HandTracking.capture)
        cv.Flip(current_frame, current_frame, 1)

        if current_frame is None:
            print('Unable to query frame from webcam device.')
            return None

        hand_skin, hand_contour, hull4defects = self.DetectHandSkin(
            current_frame)

        return self.ComputeHandPosition(hand_skin, hand_contour, hull4defects)
