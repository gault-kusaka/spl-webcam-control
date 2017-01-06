import sys
import numpy as np
import cv2


class FrameProcessor:

	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		if not self.cap.isOpened():
			raise Exception("Can't access web-camera")
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


	def get_next_frame(self):
		_, self.frame = self.cap.read()


	def erose_and_dilate(self):
		self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, np.array([2, 50, 50]), np.array([15, 255, 255]))

		dilation = cv2.dilate(mask2, kernel_ellipse, iterations=1)
		erosion = cv2.erode(dilation, kernel_square, iterations=1)    
		dilation2 = cv2.dilate(erosion, kernel_ellipse, iterations=1)    
		filtered = cv2.medianBlur(dilation2, 5)
		kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
		dilation2 = cv2.dilate(filtered, kernel_ellipse,iterations=1)
		kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
		dilation3 = cv2.dilate(filtered,kernel_ellipse, iterations=1)
		median = cv2.medianBlur(dilation2, 5)
		_, self.threshold2 = cv2.threshold(median, 127, 255, 0)

	
	def get_threshold(self):
		

		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (23, 23), 0)
		_, self.threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


	def get_hand_contour(self):
		_, self.contours, __ = cv2.findContours(self.threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		maxArea, cont = 0, None
		for i, c in enumerate(self.contours):
			area = cv2.contourArea(c)
			if area > maxArea:
				maxArea = area
				cont = c
		self.hand_contour = cv2.approxPolyDP(cont, 0.001*cv2.arcLength(cont, True), True)

	def get_hand_dims(self):
		self.hand_x, self.hand_y, self,hand_width, self.hand_height = cv2.boundingRect(self.hand_contour)


	def get_hulls(self):
		self.hull_contour = cv2.convexHull(self.hand_contour, returnPoints=False)

	def get_defects(self):
		pass