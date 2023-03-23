import cv2 as cv

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize the hand detector with the trained Haar Cascade classifier
        self.hand_cascade = cv.CascadeClassifier('path/to/haar_cascade.xml')

    def findHands(self, img, draw=True):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        hands = self.hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(hands) > 0:
            for (x, y, w, h) in hands:
                if draw:
                    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        # Convert the image to grayscale
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Detect hands in the grayscale image using the Haar Cascade classifier
        hands = self.hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # If there are no hands detected, return an empty list
        if len(hands) == 0:
            return []

        # Select the hand with the specified handNo
        (x, y, w, h) = hands[handNo]

        # Extract the hand region of interest (ROI) from the grayscale image
        hand_roi = gray[y:y+h, x:x+w]

        # Apply Gaussian blur to the hand ROI to remove noise
        hand_roi = cv.GaussianBlur(hand_roi, (5, 5), 0)

        # Apply thresholding to the hand ROI to create a binary image
        _, hand_binary = cv.threshold(hand_roi, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

        # Find the contours in the binary image
        contours, _ = cv.findContours(hand_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # If there are no contours detected, return an empty list
        if len(contours) == 0:
            return []

        # Find the contour with the largest area, which should correspond to the hand
        hand_contour = max(contours, key=cv.contourArea)

        # Find the convex hull of the hand contour
        hand_hull = cv.convexHull(hand_contour)

        # Find the hand landmarks as the points on the convex hull
        lmList = []
        for i in range(hand_hull.shape[0]):
            lmList.append([i, hand_hull[i][0][0], hand_hull[i][0][1]])
            if draw:
                cv.circle(img, (hand_hull[i][0][0]+x, hand_hull[i][0][1]+y), 5, (0, 0, 255), cv.FILLED)

        return lmList
