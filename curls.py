import cv2
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt

# cap = cv2.VideoCapture("img/curls.mp4")
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0  # 0 if gng up, 1 if gng down
prev_per = 0
e = 0
pers=[]
wrong=[]
while True:
	success, img = cap.read()
	img = cv2.resize(img, (800, 600))
	# img = cv2.imread("img/test.jpg")
	img = detector.findPose(img, False)  # remove false to see all points

	lmList = detector.findPosition(img, False)  # list of 32 points

	if len(lmList) != 0:
		angle = detector.findAngle(img, 11, 13, 15)
		per = np.interp(angle, (40, 170), (100, 0))
		pers.append(per)
		# print(angle, per)
		##ERRORS##

		if direction == 0:  # going up
			if prev_per > per:
				e += 1

			if(e == 20):
				print('Lift your arm higher')
				wrong.append(len(pers)-1)
				e = 0

		if direction == 1:  # going down
			if prev_per < per:
				e += 1

			if(e == 20):
				print('lower your arm')
				wrong.append(len(pers)-1)
				e = 0

		# counting
		if per == 100: 
			if direction == 0:
				count += 0.5
				direction = 1

		if per == 0:
			if direction == 1:
				count+=0.5
				direction = 0

		prev_per = per

		cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

x=[i for i in range(len(pers))]
y=np.array(pers)
x=np.array(x)

plt.plot(x,y)
for i in wrong:
	plt.plot(x[i],y[i],'ro')
plt.show()

cap.release()
cv2.destroyAllWindows()
