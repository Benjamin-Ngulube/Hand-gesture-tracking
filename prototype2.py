import cv2 as cv
import time
import handtrackingmodule as htm #importing hand tracking module
import pyautogui
import pygetwindow as gw

wCam,hCam=640,480

cap=cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime=0

detector1=htm.handDetector()

tipIds=[4,8,12,16,20]

while True:
    success,img=cap.read()
    img=detector1.findHands(img)
    lmList=detector1.findPosition(img,draw=False)
    win2=gw.getActiveWindowTitle()#get the current active window
    #print(lmList) #prints array showing positions of fingers held up

    if win2!=None:#to keep program form crashing when jumping from one tab to another
     check=win2.find("PowerPoint")#check if powerpoint is the current active window
     check2=win2.find("Slide")#check if powerpoint Slide Show is the current active window
  
     if check>0 or check2>0:#check if powerpoint or powerpoint slide show is open
      if len(lmList)!=0:
        fingers=[]

        #thumb
        # if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)

        #4 fingers
        for id in range(1,5):
         if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
            fingers.append(1)
         else:
            fingers.append(0)

        # print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)

        if totalFingers==1:
           pyautogui.press('left')#presses the left kaybord key

        if totalFingers==2:
           pyautogui.press('right')#presses the right keyboard key

        time.sleep(1)


    display=cv.imread('1.jpg')
    cv.putText(display,'Please press q to close program',(470,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.imshow('Program',display)
    if cv.waitKey(1) & 0xFF==ord('q'):#breaks loop when q key is pressed
        break
cap.release()
cv.destroyAllWindows() 
    