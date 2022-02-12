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
err_top=[]
err_bottom=[]
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
				err_bottom.append(angle)
				direction = 1

		if per == 0:
			if direction == 1:
				count+=0.5
				err_top.append(angle)
				direction = 0

		prev_per = per

		cv2.putText(img, str(count), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0),4)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# x=[i for i in range(len(pers))]
# y=np.array(pers)
# x=np.array(x)

# plt.plot(x,y)
# for i in wrong:
# 	plt.plot(x[i],y[i],'ro')
# plt.show()
top=np.array(err_top)
bottom=np.array(err_bottom)

x=np.array([i for i in range(max(len(err_top),len(err_bottom)))])



plt1=plt.subplot2grid((1,2),(0,0),colspan=1)
plt2=plt.subplot2grid((1,2),(0,1),colspan=1)

plt1.axhline(y = 170, color = 'r', linestyle = 'dashed',label = "minimum ideal angle at the top")
plt2.axhline(y = 40, color = 'g', linestyle = 'dashed',label = "maximum ideal angle at the bottom")
plt1.plot(np.array([i/40 for i in range(len(err_top))]),top,color="blue",linewidth = 1,label = "user position at the top")
plt2.plot(np.array([i/40 for i in range(len(err_bottom))]),bottom,color="blue",linewidth = 1, label = "user position at the top")
plt1.set_ylim(100,200)
plt2.set_ylim(30,70)

plt1.set_xlabel('time')
plt2.set_xlabel('time')

# naming the y axis
plt1.set_ylabel('accuracy')
plt2.set_ylabel('accuracy')

plt1.set_title('Accuracy of position(top)')
plt2.set_title('Accuracy of position(bottom)')


plt1.legend()
plt2.legend()
plt.show()


cap.release()
cv2.destroyAllWindows()
