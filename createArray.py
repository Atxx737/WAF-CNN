#package

from cProfile import label
import linecache
import json
from re import X
from tkinter import Y
import array as arr
import numpy as np
from PIL import Image
import random
#Define env

REQUEST_FILE='allData.txt'
PARAM_FILE='param.txt'
PAYLOAD_FILE='filter_payloay.json'

#Declare var
arr = [] #list - maybe call it array
MATRIX = 45000 # 300x150
name_img = ""

# đưa vào 1 request -> lọc param (getParam)-> so sánh với trường payload trong filter_payload.json - lấy ký tự trước dấu bằng 
# tạo 1 ma trận 170x200 các param trùng param từ request (trước dấu bằng ) -> so sánh nếu payload bằng nhau thì lấy giá trị là label của payload đấy
# nếu không bằng thì set giá trị là 0

def getParam(dataFile):
    request = open(dataFile, 'r')
    global name_img
    param =""
    lineIndex = 1
    
    for line in (request):
        if line.startswith("GET"):
            name_img = "g"
            line = line.split(' ')
            try:
                payload_formated = line[1].split('?')
                param = payload_formated[1]
                appendParam(param)
                
                arrayToMatrix(arr)
                arr.clear()
                
                
            except IndexError:
                pass
            lineIndex += 1
            
        elif line.startswith("POST"):
            name_img = "p"
            postData = linecache.getline(dataFile, lineIndex +14)
            param = postData
            appendParam(param)
            
            arrayToMatrix(arr)
            arr.clear()
            lineIndex += 1
        else:
            lineIndex += 1
                
    request.close()
   

def appendParam(param):
    param_file = open(PARAM_FILE, 'a')
    #seperate param in request
    for item in  param.split('&'):
        param_file.write(item+"/n")
        compareParam(item)  
           
    param_file.close()


def compareParam(param):
    # array_file = open(ARRAY_FILE, 'a')
    
    payload_file = open(PAYLOAD_FILE, 'r')
    payload = json.loads(payload_file.read())
    label = 0
    # param = param.strip('\n')
    if param !="":
        temp1 = param.split('=')
        for i,item in enumerate(payload['filterPayload']):
            temp2 = item['data'].split('=')
            if (temp1[0] == temp2[0]):
                if(temp1[1] == temp2[1]):
                    label = item['label']
                else:
                    label = 0
                arr.append(label)
       
    payload_file.close()
    # array_file.close()
    
def checkLengthArr(array):
    expression = len(array) - MATRIX
    if expression < 0:
        tmp = MATRIX - len(array)
        appendArray(tmp, array)
    elif expression > 0: 
        print("Array to big, it can't fix the matrix")

def appendArray(num, array):
    for i in range(num):
        array.append(0);

def arrayToMatrix(array):
    global name_img
    checkLengthArr(array)
    #code convert array to matrix
    array = np.array(array,dtype=np.uint8)
    arr_1D = list()
    for i in range (0,len(array),MATRIX):
        arr_1D.extend(array[i:i+MATRIX])
        arr_2D=np.reshape(arr_1D,(300 ,150))
        arr_1D = list()
        temp = 0
        for x in range(len(arr_2D)):
            for y in range(len(arr_2D[0])):
                if arr_2D[x,y] == 1:
                    temp = 1
                    arr_2D[x,y] = 255
                    
                # else:
                #     arr_2D[y, x] = 0
        img = Image.fromarray(arr_2D)
        if temp > 0:
            image_path = "../WAF-CNN/Picture_data/Anomaly/"
        else:
            image_path = "../WAF-CNN/Picture_data/Normal/"
            
        name_img += str(random.random())
        img.save(image_path+name_img+".png")
    
    

def main():
    getParam(REQUEST_FILE)
    
    
main()