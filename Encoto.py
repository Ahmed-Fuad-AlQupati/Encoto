from PIL import Image, ImageTk
import numpy as np
import hashlib
import tkinter as tk
from tkinter.filedialog import askopenfilename

def matrixShuf(ph:list, hashMap:list, step=0):
    
    y = ph.__len__()    
    x = len(ph[0])    
    r = x / (hashMap.__len__() / y)    
    phMatrix = np.array(ph)

    for go in range(x): 

        # shuffle rows down
        p = 0
        i = 0             
        while(p < 32):                    
            phMatrix[round(i % (y-1)),:], phMatrix[round((i + hashMap[p%32] + step) % (y-1)),:] = phMatrix[round((i + hashMap[p%32] + step) % (y-1)),:].copy(), phMatrix[round(i % (y-1)),:].copy()           
            p += 1
            i += r


        # shuffle Columns down
        p = 0      
        j = 0    
        while(p < 32):        
            phMatrix[:,round(j % (x-1))], phMatrix[:,round((j + hashMap[p%32] + step) % (x-1))] = phMatrix[:,round((j + hashMap[p%32] + step) % (x-1))].copy(), phMatrix[:,round(j % (x-1))].copy()
            p += 1
            j += r
        step += 1
    ph.clear()    
    ph.extend( phMatrix.tolist() )     


def enc(ph:list,key):
    y = ph.__len__()
    x = len(ph[0])    
    move = []
            
    for ch in key:                
        move.append(ord(ch) % x)
    
    matrixShuf(ph, move)



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
    
key = "asdafaf"
hashKey = hashlib.md5(key.encode()).hexdigest()

asd = tk.Tk()

try:
    img = openImageAsMatrix()
    img = matrix2List(img)
    enc(img, hashKey)

except:
    exit()





img = list2Matrix(img)

can = tk.Canvas(asd, width=img.shape[1], height=img.shape[0])
can.pack(expand=True)
pilImage = Image.fromarray(np.uint8(img))
tkImage = ImageTk.PhotoImage(pilImage)
can.create_image(0,0, anchor="nw", image=tkImage)

asd.mainloop()
        