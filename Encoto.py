from PIL import Image, ImageTk
from numpy import array,uint8, uint16
from hashlib import md5
from tkinter import Tk, Frame, Canvas, Label, Entry, Button, Checkbutton
from tkinter.ttk import Progressbar
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter.filedialog import askopenfilename, asksaveasfilename

def matrixShuf(ph:list, hashMap:list, step=0):
    global imgList, imgMatrix
    
    y = ph.__len__()    
    x = len(ph[0])    
    r = x / (hashMap.__len__() / y)    
    phMatrix = array(ph)    
    
    for go in range(x):   
        
        progressBar.config(value=(100/x)*go)
        progressBar.update()
        
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
    phMatrix = array(ph)        
    step = x-1    
    for go in range(x): 
        
        progressBar.config(value=(100/x)*go)
        progressBar.update()        
        
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
    hashKey = md5(key.get().encode()).hexdigest()    
            
    for ch in hashKey:                
        move.append(ord(ch) % x)
    
    progressBar.place(x=10, y=15) 
    matrixShuf(ph, move)    
    showImageCanvas(imgMatrix) 
    progressBar.config(value=0)
    progressBar.place_forget()

def dec(ph:list):
    global imgList, imgMatrix
    if(key.get() == ""):
        showerror("Key Error", "Key Can't Be Blank")
        key.focus()
        return
    
    y = ph.__len__()
    x = len(ph[0])    
    move = []
    hashKey = md5(key.get().encode()).hexdigest()    
    
    for ch in hashKey:                
        move.append(ord(ch) % x) 
    
    
    progressBar.place(x=10, y=15)
    matrixUnShuf(ph, move)
    showImageCanvas(imgMatrix)
    progressBar.config(value=0)
    progressBar.place_forget()

def matrix2List(imgMatrix):    
    imgList = imgMatrix.tolist()
    return imgList

def list2Matrix(imgList):
    imgMatrix = array(imgList)
    return imgMatrix  


def openImageAsMatrix():
    global saved
    if(not saved):
        if(not askokcancel("Open Photo", "You Didn't Save The Photo Yet, The Changes will be lost.\nDo You Open Another Photo")):
            return
    global imgMatrix, imgList, fileName
    path = askopenfilename(title = "Select Photo", filetypes = (("Image Files","*.png;*.jpg;*.jpeg"),))
    if(path):             
        imgPil = Image.open(path)
        imgMatrix = array(imgPil, dtype=uint8)
        imgList = matrix2List(imgMatrix)
        showImageCanvas(imgMatrix)
        encButton.config(state="n")
        decButton.config(state="n")
        saveButton.config(state="n")
        saved = False
        fileName = str(path).split("/")[-1]
        key.focus()
        

def saveImagefromMatrix():
    global imgMatrix, saved      
    path = asksaveasfilename(initialfile=fileName,title="Save Photo", filetypes=(("PNG Image files","*.png"),),)
    if(path):                
        pilImage = Image.fromarray(uint8(imgMatrix))        
        pilImage.save(path.replace(".png", "")+".png") 
        showinfo("Save Photo", "The Photo Saved Successfully.")
        saved = True
        
def scaleImage(img:Image, maxX,maxY):
    x,y = img.size
    aspRatio = y/x
    y = maxY
    x = int(y / aspRatio)
    return img.resize((x,y),)



def showImageCanvas(imgMatrix):
    global pilImage, tkImage, can
    pilImage = Image.fromarray(uint8(imgMatrix))    
    pilImage = scaleImage(pilImage, 700,450)
    tkImage = ImageTk.PhotoImage(pilImage)    
    can.create_image(0,0, anchor="nw", image=tkImage)
    


def restore():         
    dec(img, hashKey)
    imgMatrix = list2Matrix(img)
    showImageCanvas(imgMatrix)

def showKey():
    if(key.cget("show")):
        key.config(show="")
        cKey.deselect()
    else:
        key.config(show="*")
        cKey.select()


#######################
if __name__ == "__main__":
    
    saved = True
    
    asd = Tk()    
    asd.geometry(f"800x600+{asd.winfo_screenwidth()//2-400}+{asd.winfo_screenheight()//2-300}")
    asd.resizable(False, False)
    asd.title(":Encoto:")    
    
    top = Frame(asd, bg="#333")
    top.pack(fill="x")
    body = Frame(asd, bg="#333")
    body.pack(fill="both", expand=True)
    low = Frame(asd, bg="#345")
    low.pack(fill="x")
    
    Label(top, text=":: Encoto ::", font=("",32,""), bg="#333", fg="#fea" ).pack()
    progressBar = Progressbar(top, value=0, length=200)
    
    
    
    can = Canvas(body, bg="#333", borderwidth=10)
    can.pack(expand=True, fill="both")
    
    selectAndSaveFrame = Frame(low, bg="#345")
    selectAndSaveFrame.pack(side="right", padx=10)
    openButton = Button(selectAndSaveFrame, text = "Choose Photo", font=("", 12, "italic"), width=13, command=openImageAsMatrix)
    openButton.pack()
    saveButton = Button(selectAndSaveFrame, text = "Save Photo", font=("", 12, "italic"), width=13,   command=saveImagefromMatrix)
    saveButton.pack(pady=(5,0))
    saveButton.config(state="d")
    
    encDecFrame = Frame(low, bg="#345")
    encDecFrame.pack(side="left", padx=10)
    encButton = Button(encDecFrame, text = "<< Encrypting >>", font=("", 12, "bold"), command=(lambda:enc(imgList)))
    encButton.pack(side="left", padx=(10,0))
    encButton.config(state="d")
    decButton = Button(encDecFrame, text = ">> Decrypting <<", font=("", 12, "bold"), command=(lambda:dec(imgList)))
    decButton.pack(side="left", padx=(10,0))
    decButton.config(state="d")
    
    
    keyFrame = Frame(low, bg="#345")
    keyFrame.pack( padx=10, pady=30)
    Label(keyFrame, text="Encr Key:",font=("", 10, "bold"), bg="#345", fg="#fea").pack(anchor="sw")
    key = Entry(keyFrame,font=("", 12, "bold"), show="*")
    key.pack(side="left")
    
    cKey = Checkbutton(keyFrame, bg="#345", command=showKey, activebackground="#345")
    cKey.pack(side="right")
    cKey.select()
    
    asd.mainloop()    