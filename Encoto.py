def arrPrint(arr, x, y):
    for I in range(y):
        for i in range(x):
            print(arr[I][i], end=" ") 
        print()

def shuf(ph:list, hashMap:list, step=0):
    y = ph.__len__()    
    x = len(ph[0])    
    r = x / (32 / y) 
    
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
        
    if(step < x):
        shuf(ph, hashMap, step+1)


def enc(ph:list,key):
    y = ph.__len__()
    x = len(ph[0])    
    move = []
            
    for ch in key:                
        move.append(ord(ch) % x)
    
    shuf(ph, move)
                
    
    
x = []
c = 1
for I in range(14):
    x.append([])
    for i in range(13):
        #x[I].append(c)
        #c += 1
        if(i < 3):
            x[I].append("r")
        elif (i < 6):
            x[I].append("g")
        else:
            x[I].append("b")
            

arrPrint(x, len(x[0]), len(x))
    
key = "ahmed"
import hashlib
hashKey = hashlib.md5(key.encode()).hexdigest()

enc(x, hashKey)
print("\n")

arrPrint(x, len(x[0]), len(x))