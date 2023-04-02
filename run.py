import cv2
import numpy as np
import math
import json
import redis
import jsonpickle
import pymysql

device ='http://192.168.0.6:4747/video'
cap = cv2.VideoCapture(device)
whT = 320
#gps = gpsmodul

rd = redis.StrictRedis(host='localhost',port=6379, db=0)

#conn = pymysql.connect(
#    host='192.168.0.2',
#    user='project',
#    password='1234',
#    db="crosswalk"
#)


def location_write(value):
    dataDict = {value} #gps input
    jsonDataDict = jsonpickle.encode(dataDict)
    rd.set(rd.dbsize(), jsonDataDict)
    resultData = rd.get(rd.dbsize())
    resultData = jsonpickle.decode(resultData)

    
#def location_sync():
    
confThreshold_1 = 0.9
confThreshold_2 = 0.5
nmsThreshold = 0.05

classesFile = 'obj.names'

with open(classesFile, 'rt') as f:
        classNames = f.read().split('\n')

model_config = 'yolo-obj.cfg'
model_weights = 'yolo-obj2_last6800.weights'

net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold_1:
                w, h = int(det[2]*wT), int(det[3]*hT)
                x, y = int((det[0]*wT) - w/2), int((det[1]*hT) - h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
          
        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold_2, nmsThreshold)
    print(f"식별된 대상 : {len(indices)} 개")
    
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, f"{classNames[classIds[i]].upper()} {int(confs[i]*100)}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if classNames[classIds[i]] == 'crosswalk':
           print("detect crosswalk")
           location_write('37.1 128.9')

        if classNames[classIds[i]] == 'red':
           print("detect red")

        if classNames[classIds[i]] == 'green':
           print("detect green")
    
def guideCrosswalk(userx , usery):
    a = txt[0] - uesrx
    b = txt[1] - usery
    c = math.sqrt((a * a) + (b * b)) 
    if c < 0.0002:
        txt

def isCrosswalk(txt,value): #There is a crosswalk nearby
    f = txt
    while True:
        f.readlines() 

        if length >= value:

            return false

        if length < value:

            return true


def findCrosswalk():
    f = open('location.txt','a')
    lat = gps.lat
    long = gps.long
    a = lat - txt
    b = txt[1] - usery
    c = math.sqrt((a * a) + (b * b))

    if isCrosswalk(f):
        txt.writelines([lat,long])
        txt.write('\n')
        f.close()

    

#def gps
    #return lat,long,delection1,delection2

while True:
    success, img = cap.read()
    
    if not success:
        break
    
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], True, crop=False)
    net.setInput(blob)
    
    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    
    findObjects(outputs, img)
    
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        f.close()
        break
