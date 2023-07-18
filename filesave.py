def saveimg(image,temp):
    
    import os
    if not os.path.exists("images"):
      
        os.makedirs("images/")

    import datetime,cv2
    timenow = "images/"+str(datetime.datetime.now())+"__"+temp+".jpg"
    cv2.imwrite(timenow,image)
