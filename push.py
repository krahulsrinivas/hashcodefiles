import cv2
import numpy as np
import time
import PoseModule as pm


cap = cv2.VideoCapture("img/pushr.mp4")
# cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0  # 0 if gng down, 1 if gng up
prev_per = 0
e = 0

l1 = []
l2 = []

while True:
	success, img = cap.read()
	img = cv2.resize(img, (800, 600))
	img = detector.findPose(img, False)  # remove false to see all points

	lmList = detector.findPosition(img, False)  # list of 32 points

	if len(lmList) != 0:
		elbowAngle = detector.findAngle(img, 12, 14, 16)
		buttAngle = detector.findAngle(img, 12, 24, 26)
		legAngle = detector.findAngle(img, 24, 26, 28)
		#elbowAngle = detector.findAngle(img, 11, 13, 15)
		#buttAngle = detector.findAngle(img, 11, 23, 25)
		#legAngle = detector.findAngle(img, 23, 25, 27)

		per = np.interp(elbowAngle, (80, 160), (100, 0))
		# print(angle, per)
		##ERRORS##
		if direction == 0:
			# elbow>165
            # but>160
            # leg>170
			if legAngle<160:
				#cv2.putText(img, "make ur legs straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)
				print('make ur legs straighter')
			if buttAngle<165:
				#cv2.putText(img, "make ur butt straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)
				print('make your back straight.')          
			
			if prev_per > per: 
				e+=1

			if(e == 20):
				print('bring your chest closer to the ground!')
				e= 0
				
		if direction == 1:#going up
			# elbow<40
            # but>160
            # leg>170
			if legAngle<160:
				#cv2.putText(img, "make ur legs straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)
				print('make ur legs straighter')
			if buttAngle<170:
				#cv2.putText(img, "make ur butt straighter", (0,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)
				print('make your back straight.')              

			if(prev_per > per):
				e+=1
			if(e==30):
				print('Higher! Straighten your hands')
				e= 0
                	
		# counting
		if elbowAngle <= 70: 
			if direction == 0:
				count += 0.5
				direction = 1

		if elbowAngle >= 165:
			if direction == 1:
				count+=0.5
				direction = 0

		prev_Angle = elbowAngle
		cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()