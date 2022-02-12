import cv2
import numpy as np
import time
import PoseModule as pm
 

cap = cv2.VideoCapture("img/plank2.mp4")
#cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
e1 = 0
e2=0
e22=0
e3=0

while True:
	success, img = cap.read()
	#img = cv2.resize(img, (800,600))
	#img = cv2.imread("img/plank.jpg")
	img = detector.findPose(img,False) # remove false to see all points

	lmList = detector.findPosition(img, False) #list of 32 points
	if len(lmList) != 0:
		angle1 = detector.findAngle(img, 11, 13, 15)#	elbow
		angle2 = detector.findAngle(img, 11, 23, 25)#   hip
		angle3 = detector.findAngle(img, 23, 25, 27)#	legs


		#x`print(angle1, angle2, angle3)
		if not 75<=angle1<=105:
			e1+=1
		if(e1==30):
			print('Bring your shoulder vertically above your elbow')
			e1 = 0

		if angle2<150:
			e2+=1
		if(e2==30):
			print('Make your back straight. Bring your buttocks DOWN')
			e2 = 0 

		if angle2 > 168:
			e22+=1
		if(e22==20):
			print('Make your back straight. Bring your buttocks UP')
			e2=0


		if angle3<=160 :
			e3+=1
		if(e3==20):
			print('Do not bend your knee. Stretch your legs')
			e3 = 0


		#cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()