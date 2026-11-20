from PIL import Image, ImageTk
import numpy as np
import hashlib
import tkinter as tk
from tkinter.filedialog import askopenfilename

def arrPrint(arr, x, y):
    for I in range(y):
        for i in range(x):
            print(arr[I][i], end=" ") 
        print()

def shuf(ph:list, hashMap:list, step=0):
    y = ph.__len__()    
    x = len(ph[0])    
    r = x / (32 / y)     
    
    for s in range((x*y)//2):
        
        # shuffle x down
        p = 0
        i = 0  
        j = 0    
        while(i < y):        
            while(p < 32):            
                ph[i][round(j)], ph[i][round((j + hashMap[p] + step) % (x-1))] = ph[i][round((j + hashMap[p] + step) % (x-1))], ph[i][round(j)]
                if(j + r > x):
                    j = (j + r) % (x-1)
                    p += 1
                    break
                j = (j + r) % (x-1)
                p += 1        
            i += 1     
        # shuffle x up
        p = 0
        i = y-1  
        j = 0                
        while(i >= 0):        
            while(p < 32):            
                ph[i][round(j)], ph[i][round((j + hashMap[p] + step) % (x-1))] = ph[i][round((j + hashMap[p] + step) % (x-1))], ph[i][round(j)]
                if(j + r > x):
                    j = (j + r) % (x-1)
                    p += 1
                    break
                j = (j + r) % (x-1)
                p += 1        
            i -= 1
        
        # shuffle y down   
        p = 0
        i = 0  
        j = 0                
        while(j < x):        
            while(True):
                ph[round(i)][j], ph[round((i+hashMap[p] + step) % (y-1))][j] = ph[round((i+hashMap[p] + step) % (y-1))][j], ph[round(i)][j]
                if(i + r > x):
                    i = (i + r) % (y-1)
                    p = (p + 1) % (hashMap.__len__()-1)
                    break
                i = (i + r) % (y-1)
                p = (p + 1) % (hashMap.__len__()-1)
            j += 1
    
        # shuffle y up
        p = 0
        i = 0  
        j = x-1               
        while(j >= 0):        
            while(p < 32):
                ph[round(i)][j], ph[round((i+hashMap[p] + step) % (y-1))][j] = ph[round((i+hashMap[p] + step) % (y-1))][j], ph[round(i)][j]
                if(i + r > x):
                    i = (i + r) % (y-1)
                    p += 1
                    break
                i = (i + r) % (y-1)
                p += 1          
            j -= 1  
        step += 1    
    #if(step < x*y):
        #shuf(ph, hashMap, step+1)


def enc(ph:list,key):
    y = ph.__len__()
    x = len(ph[0])    
    move = []
            
    for ch in key:                
        move.append(ord(ch) % x)
    
    shuf(ph, move)



def openImageAsMatrix():
    extensions = [".jpg", ",jpeg", ".png"]
    fileTypes = []
    for i in extensions:
        fileTypes.append((i[1:], "JPG or PNG Image"))
        
    path = askopenfilename(title = "Select Photo", filetypes = fileTypes)
    img = Image.open(path)
    imgMatrix = np.array(img, dtype=np.uint8)
    return imgMatrix
   
def matrix2List(imgMatrix):    
    imgList = imgMatrix.tolist()
    return imgList

def list2Matrix(imgList):
    imgMatrix = np.array(imgList)
    return imgMatrix                     
    
key = "asd"
hashKey = hashlib.md5(key.encode()).hexdigest()

img = openImageAsMatrix()
img = matrix2List(img)
enc(img, hashKey)

 



asd = tk.Tk()

img = list2Matrix(img)

can = tk.Canvas(asd, width=img.shape[1], height=img.shape[0])
can.pack(expand=True)
pilImage = Image.fromarray(np.uint8(img))
tkImage = ImageTk.PhotoImage(pilImage)
can.create_image(0,0, anchor="nw", image=tkImage)

asd.mainloop()
        