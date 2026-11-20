from PIL import Image, ImageTk
import numpy as np
import hashlib
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename


def matrixShuf(ph:list, hashMap:list, step=0):
    global imgList, imgMatrix
    
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

        #shuffle Columns down
        p = 0      
        j = 0    
        while(p < 32):        
            phMatrix[:,round(j % (x-1))], phMatrix[:,round((j + hashMap[p%32] + step) % (x-1))] = phMatrix[:,round((j + hashMap[p%32] + step) % (x-1))].copy(), phMatrix[:,round(j % (x-1))].copy()
            p += 1
            j += r
            
        step += 1        
    ph.clear()    
    ph.extend( phMatrix.tolist() )
    imgMatrix = list2Matrix(ph)    


def matrixUnShuf(ph:list, hashMap:list, step=0):
    global imgList, imgMatrix
    y = ph.__len__()    
    x = len(ph[0])    
    r = x / (hashMap.__len__() / y)    
    phMatrix = np.array(ph)        
    step = x-1    
    for go in range(x): 
        progress.set( (100 / x) * go )
        # Unshuffle Columns down
        p = 31      
        j = r * 31    
        while(p > -1):        
            phMatrix[:,round(j % (x-1))], phMatrix[:,round((j + hashMap[p%32] + step) % (x-1))] = phMatrix[:,round((j + hashMap[p%32] + step) % (x-1))].copy(), phMatrix[:,round(j % (x-1))].copy()
            p -= 1
            j -= r            
        
        # Unshuffle rows down
        p = 31
        i = r * 31             
        while(p > -1):                    
            phMatrix[round(i % (y-1)),:], phMatrix[round((i + hashMap[p%32] + step) % (y-1)),:] = phMatrix[round((i + hashMap[p%32] + step) % (y-1)),:].copy(), phMatrix[round(i % (y-1)),:].copy()           
            p -= 1
            i -= r
        step -= 1        
    ph.clear()    
    ph.extend( phMatrix.tolist() )        
    imgMatrix = list2Matrix(ph)

def enc(ph:list):
    global imgList, imgMatrix
    if(key.get() == ""):
        showerror("Key Error", "Key Can't Be Blank")
        key.focus()
        return
    
    y = ph.__len__()
    x = len(ph[0])    
    move = []
    hashKey = hashlib.md5(key.get().encode()).hexdigest()    
            
    for ch in hashKey:                
        move.append(ord(ch) % x)
    
    matrixShuf(ph, move)    
    showImageCanvas(imgMatrix)    

def dec(ph:list):
    if(key.get() == ""):
        showerror("Key Error", "Key Can't Be Blank")
        key.focus()
        return
    
    y = ph.__len__()
    x = len(ph[0])    
    move = []
    hashKey = hashlib.md5(key.get().encode()).hexdigest()    
    
    for ch in hashKey:                
        move.append(ord(ch) % x)    
    matrixUnShuf(ph, move)
    showImageCanvas(imgMatrix)


def matrix2List(imgMatrix):    
    imgList = imgMatrix.tolist()
    return imgList

def list2Matrix(imgList):
    imgMatrix = np.array(imgList)
    return imgMatrix  


def openImageAsMatrix():
    global imgMatrix, imgList
    extensions = [".jpg", ",jpeg", ".png"]
    fileTypes = []
    for i in extensions:
        fileTypes.append((i[1:], "JPG or PNG Image"))
        
    path = askopenfilename(title = "Select Photo", filetypes = fileTypes)
    if(path):             
        imgPil = Image.open(path)
        imgMatrix = np.array(imgPil, dtype=np.uint8)
        imgList = matrix2List(imgMatrix)
        showImageCanvas(imgMatrix)


def scaleImage(img:Image, maxX,maxY):
    x,y = img.size
    aspRatio = y/x
    if(y > maxY):
        y = maxY
        x = int(y / aspRatio)
    elif(x > maxX):
        x = maxX
        y = int(x / aspRatio)
    
    return img.resize((x,y),)



def showImageCanvas(imgMatrix):
    global pilImage, tkImage, can
    pilImage = Image.fromarray(np.uint8(imgMatrix))
    pilImage = scaleImage(pilImage, 700,500)
    tkImage = ImageTk.PhotoImage(pilImage)    
    can.create_image(0,0, anchor="nw", image=tkImage)
    
    

    
    
        
    
    
    #pilImage.save("path\\enc.png")

def restore():         
    dec(img, hashKey)
    imgMatrix = list2Matrix(img)
    showImageCanvas(imgMatrix)









asd = tk.Tk()

asd.geometry(f"800x600+{asd.winfo_screenwidth()//2-400}+{asd.winfo_screenheight()//2-300}")
asd.resizable(False, False)
asd.title(":Encoto:")

top = tk.Frame(asd, bg="#333")
top.pack(fill="x")
body = tk.Frame(asd, bg="#333")
body.pack(fill="both", expand=True)
low = tk.Frame(asd, bg="#345")
low.pack(fill="x")

tk.Label(top, text=":: Encoto ::", font=("",32,""), bg="#333", fg="#fea" ).pack()
can = tk.Canvas(body, bg="#333", borderwidth=10)
can.pack(expand=True, fill="both")
tk.Button(low, text = "Choose Image", font=("", 12, "italic"), command=openImageAsMatrix).pack(side="right" ,padx=(0,10))
tk.Button(low, text = "<< Encrypting >>", font=("", 12, "bold"), command=(lambda:enc(imgList))).pack(side="left", padx=(10,0))
tk.Button(low, text = ">> Decrypting <<", font=("", 12, "bold"), command=(lambda:dec(imgList))).pack(side="left", padx=(10,0))
tk.Label(low, text="Encr Key:",font=("", 10, "bold"), bg="#345", fg="#fea").pack(anchor="s",expand=True, padx=(0,120))
key = tk.Entry(low,font=("", 12, "bold"))
key.pack(anchor="center",expand=True, pady=(0,35))

asd.mainloop()