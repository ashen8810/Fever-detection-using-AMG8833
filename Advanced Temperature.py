import time,sys
sys.path.append('../')
# load AMG8833 module
import amg8833_i2c
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import imutils


t0 = time.time()
sensor = []
while (time.time()-t0)<1: # wait 1sec for sensor to start
    try:
        # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
        sensor = amg8833_i2c.AMG8833(addr=0x69) # start AMG8833
    except:
        sensor = amg8833_i2c.AMG8833(addr=0x68)
    finally:
        pass
pix_res = (8,8)# wait for sensor to settle
xx,yy = (np.linspace(0,pix_res[0],pix_res[0]),
                    np.linspace(0,pix_res[1],pix_res[1]))
zz = np.zeros(pix_res) # set array with zeros first
# new resolution
pix_mult = 18
wi=he = pix_mult*8# multiplier for interpolation 
interp_res = (int(pix_mult*pix_res[0]),int(pix_mult*pix_res[1]))
grid_x,grid_y = (np.linspace(0,pix_res[0],interp_res[0]),
                            np.linspace(0,pix_res[1],interp_res[1]))
# interp function
def interp(z_var):
    # cubic interpolation on the image
    # at a resolution of (pix_mult*8 x pix_mult*8)
    f = interpolate.interp2d(xx,yy,z_var,kind='cubic')
    return f(grid_x,grid_y)
 # interpolated image
import cv2
pix_to_read = 64 # read all 64 pixels
vs = cv2.VideoCapture(-1)
print("[INFO] starting video stream...")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
temp=[35]
t = 35
caliberation = 7.8
while True:
    time.sleep(0.1)
    _,image = vs.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imag =cv2.resize(image, (wi,he), 
               interpolation = cv2.INTER_LINEAR)
    imag = cv2.flip(imag, 1)
   
    status,pixels = sensor.read_temp(pix_to_read) # read pixels with status
    if status: # if error in pixel, re-enter loop and try again
        continue
    
    new_z = interp(np.reshape(pixels,pix_res)) # interpolated image
   
    eyes = eye_cascade.detectMultiScale(imag,1.04,2)

    for (ex,ey,ew,eh) in eyes:
        try:
            
        #cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            cc = new_z[ey:ey+eh+5,ex+10:ex+ew+5]
            t=np.amax(cc)+caliberation
            t =round(t,2)
            temp.append(t)
            
        except:
            pass
    #cv2.rectangle(image, (ex, ey), (ex+ew, ey+eh), (0,0,255), 1)
    try:
        
        cv2.putText(image, str(round(sum(temp)/len(temp),2)) + ' oC', (ex,ey+10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255),2)
    except:
        pass
    try:
        if len(temp)>3 or sum(temp)/len(temp) > 38:
            print(sum(temp)/len(temp))
           
        
            if sum(temp)/len(temp) > 38:
                flag = True
                cv2.putText(image, 'Warning!!!!!!', (ex, ey+30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),2)
                #from Buzzer import buzz
                #buzz()
                #from filesave import saveimg
                #try:
                #    saveimg(image,str(round(sum(temp)/len(temp),2)))
                #except Exception as e:
                #    print(e)
                
            else:
                flag = False
                
            temp.clear()
           
    except Exception as e:
       
        pass
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

   