# Camera.py
# File that contains functions:
    # takePic() - takes picture from camera
    # converImage64(image) - encodes image into byte 64
    # sendImage() - combines above two functions, takes pic, returns the encoded value
    

import cv2
import numpy as np
import base64

# 0: main camera, 1: external camera -> when using raspberry pi switch to 0 i think
cameraSource = 0
cam = cv2.VideoCapture(cameraSource)

def takePic():
    # initialize camera
    
    # open camera
    result, image = cam.read()
    
    # if able to open camera show the image
    if result:
        # show image
        # cv2.imshow("Image", image)
        
        # get rid of image window by pressing y
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord('y'):
        #     cv2.destroyAllWindows()
        
        # image type: numpy.ndarray
        # cv2.imwrite('new_image.jpg', image)
        return image
    
    # not able to open camera; print error
    else:
        print("Can't get image")
        return -1
    
# image parameter: numpy.ndarray
def convertImage64(image):
    retval, buffer = cv2.imencode('.jpg', image)
    image64_String = base64.b64encode(buffer).decode("utf-8")
    return image64_String

# function to send over image, call API to send over?
def sendImage():
    print("Taking picture")
    imageNDArray = takePic()
    print("Converting to base64")
    image64_String = convertImage64(imageNDArray)
    print(image64_String[:10])
    return image64_String

# MAIN FOR TESTING 
# count = 0
# while count == 0:
    
    
#     img = sendImage()
    
#     # DEBUG: Testing to see if file conversion worked
#     # opening file and writing to it
#     f = open("base64.jpg", "wb")
#     imgJpg = base64.b64decode(img)
#     f.write(imgJpg)
#     f.close()
    
#     count += 1
