
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
from Adafruit_AMG88xx import Adafruit_AMG88xx
import numpy as np

# init calib parameter for thermal sensor
calib = 7

# define classifier
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# init AMG8833 thermal sensor
sensor = Adafruit_AMG88xx()

# start video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0,resolution=(64,64)).start()

time.sleep(0.1)

fps = FPS().start()

from time import sleep
temp=[]
while True:
    
    # read temperature
    pixels = sensor.readPixels()
    
    max_temp = np.amax(pixels) + calib
    image = vs.read()

    bboxes = classifier.detectMultiScale(image)
    
    # print bounding box for each detected face
    for box in bboxes:
      # extract
      x, y, width, height = box
      x2, y2 = x + width, y + height
      # draw rectangle over the pixels
     # cv2.rectangle(image, (x, y), (x2, y2), (0,0,255), 1)
      text_pos = y - 15 if y - 15 >15 else y+ 15
      
      max_temp =round(max_temp,2)
      temp.append(max_temp)
      temp_text = str(max_temp)
      cv2.putText(image, str(round(sum(temp)/len(temp),2)) + ' oC', (x, text_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255),2)
      break
    

    try:
        if len(temp)>3 or sum(temp)/len(temp) > 38.2:
            print(sum(temp)/len(temp))
        
            if sum(temp)/len(temp) > 38.2:
                cv2.putText(image, 'Warning!!!!!!', (x, text_pos+20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),2)
                print(round(sum(temp)/len(temp),2))
                #from Buzzer import buzz
                #buzz()
                #from filesave import saveimg
                #try:
                #    saveimg(image,str(round(sum(temp)/len(temp),2)))
                #except Exception as e:
                #    print(e)
                
            temp.clear()
    except Exception as e:
        print(e)
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
    fps.update()

fps.stop()
cv2.destroyAllWindows()
vs.stop()
