from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter import ttk
import numpy as np
import os.path

root = Tk()
fileName = 'empty' # Tuple for all filenames that has been selected
idx = 0 # Index for the current image
imageWidth,imageHeight = 1344,1024
# Show on the progress label 'current image index/the whole number of loaded 
# image.
currAll = StringVar()  
currAll.set('0/0')
markR = 3 # Mark radius
backLeng = 8 # the length of the back part of the filename which is different in a same set


def loadFileName():
    global fileName, idx
    idx = 0
    fileName = filedialog.askopenfilename(multiple=True)
    image = Image.open(fileName[idx])
    canvas.background = ImageTk.PhotoImage(image=image)
    currImage = canvas.create_image((0,0),image=canvas.background,anchor=NW,tags='image')
    currAll.set('%d / %d' % (idx+1,len(fileName)) )
    canvas.delete('marks')
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    if os.path.isfile(coorName):
        # coordinates of all marks of the current image
        markCoor = np.load(coorName) 
        for oneCoor in markCoor: 
            canvas.create_oval(oneCoor[0]-markR,oneCoor[1]-markR,oneCoor[0]+markR,oneCoor[1]+markR,\
                                         fill='red',tags=('marks'))
            
        
    
    
def showNextImage():
    global idx
    idx += 1
    if idx == len(fileName):
        idx = 0
    image = Image.open(fileName[idx])
    canvas.background = ImageTk.PhotoImage(image=image)
    currImage = canvas.create_image((0,0),image=canvas.background,anchor=(NW),tags='image')
    currAll.set('%d / %d' % (idx+1,len(fileName)) )
    canvas.delete('marks')
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    if os.path.isfile(coorName):
        # coordinates of all marks of the current image
        markCoor = np.load(coorName) 
        for oneCoor in markCoor: 
            canvas.create_oval(oneCoor[0]-markR,oneCoor[1]-markR,oneCoor[0]+markR,oneCoor[1]+markR,\
                                         fill='red',tags=('marks'))

def showPrevImage():
    # Show previous image
    global idx
    idx -= 1
    # Show the last image if the current image is the first one
    if idx == -1:
        idx = len(fileName)-1
    image = Image.open(fileName[idx])
    canvas.background = ImageTk.PhotoImage(image=image)
    currImage = canvas.create_image((0,0),image=canvas.background,anchor=(NW),tags='image')  
    currAll.set('%d / %d' % (idx+1,len(fileName)) )
    canvas.delete('marks')
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    if os.path.isfile(coorName):
        # coordinates of all marks of the current image
        markCoor = np.load(coorName) 
        for oneCoor in markCoor: 
            canvas.create_oval(oneCoor[0]-markR,oneCoor[1]-markR,oneCoor[0]+markR,oneCoor[1]+markR,\
                                         fill='red',tags=('marks'))

def showPrevSet():
    # Show previous image
    global idx
    setLeng = 15 # setleng = set length
    idx = idx - idx%setLeng 
    idx -= setLeng   
    # Show the last image if the current image is the first one
    if idx < 0:
        idx = len(fileName)-setLeng-1
    # move index to the middle(most clearest one) one of the set
    idx += int(setLeng/2)
    image = Image.open(fileName[idx])
    canvas.background = ImageTk.PhotoImage(image=image)
    currImage = canvas.create_image((0,0),image=canvas.background,anchor=(NW),tags='image')  
    currAll.set('%d / %d' % (idx+1,len(fileName)))
    canvas.delete('marks')
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    if os.path.isfile(coorName):
        # coordinates of all marks of the current image
        markCoor = np.load(coorName) 
        for oneCoor in markCoor: 
            canvas.create_oval(oneCoor[0]-markR,oneCoor[1]-markR,oneCoor[0]+markR,oneCoor[1]+markR,\
                                         fill='red',tags=('marks'))
    
def showNextSet():
    global idx
    setLeng = 15 # setleng = set length
    idx = idx - idx%setLeng 
    idx += setLeng   
    # Show the last image ifL the current image is the first one
    if idx >= len(fileName):
        idx = 0
    # move index to the middle(most clearest one) one of the set
    idx += int(setLeng/2)
    image = Image.open(fileName[idx])
    canvas.background = ImageTk.PhotoImage(image=image)
    currImage = canvas.create_image((0,0),image=canvas.background,anchor=(NW),tags='image')  
    currAll.set('%d / %d' % (idx+1,len(fileName)))
    canvas.delete('marks')
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    if os.path.isfile(coorName):
        # coordinates of all marks of the current image
        markCoor = np.load(coorName) 
        for oneCoor in markCoor: 
            canvas.create_oval(oneCoor[0]-markR,oneCoor[1]-markR,oneCoor[0]+markR,oneCoor[1]+markR,\
                                         fill='red',tags=('marks'))    
    
def mark(event):
    global markR
    canvas.create_oval(event.x-markR,event.y-markR,event.x+markR,event.y+markR,fill='red',tags=('marks'))
    allMark = canvas.find_withtag('marks')
    # Mark coordinate, an numpy array to store all the marked coordinate
    markCoor = np.empty((1,2),dtype=np.int16) 
    for oneMark in allMark:
        oneCoor = canvas.coords(oneMark) # the coordinate of one mark
        x = np.int16((oneCoor[0]+oneCoor[2])/2)
        y = np.int16((oneCoor[1]+oneCoor[3])/2)
        markCoor = np.append(markCoor,np.array([[x,y]]),axis=0)
    markCoor = markCoor[1:]
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    markCoor.dump(coorName)
    
def delMark(event): # delete mark
    xNear, yNear = 2000,2000 # Initial distance on x,y direction
    allMark = canvas.find_withtag('marks')
    if len(allMark)>0:
        for oneMark in allMark:
            oneCoor = canvas.coords(oneMark) # the coordinate of one mark
            x = np.int64((oneCoor[0]+oneCoor[2])/2)
            y = np.int64((oneCoor[1]+oneCoor[3])/2)
            xDist = event.x-x # x distance
            yDist = event.y-y # y distance
            if xDist**2+yDist**2 < xNear**2+yNear**2:
                xNear = xDist
                yNear = yDist
                nearMark = oneMark # the nearest mark
        canvas.delete(nearMark)
    allMark = canvas.find_withtag('marks')
    markCoor = np.empty((1,2),dtype=np.int16) 
    for oneMark in allMark:
        oneCoor = canvas.coords(oneMark) # the coordinate of one mark
        x = np.int16((oneCoor[0]+oneCoor[2])/2)
        y = np.int16((oneCoor[1]+oneCoor[3])/2)
        markCoor = np.append(markCoor,np.array([[x,y]]),axis=0)
    markCoor = markCoor[1:]
    coorName = fileName[idx][0:-backLeng]+'.dat' # the name of the coordinate file
    markCoor.dump(coorName)

        
    

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

canvas = Canvas(root,width=imageWidth+20,height=imageHeight+20)
canvas.grid(column=0, row=0,rowspan=4, sticky=(N, W))
canvas.bind('<Button-1>',mark)    
canvas.bind('<Button-3>',delMark)





openImage = ttk.Button(root,text='Open',command=loadFileName) 
openImage.grid(column=1,row=0)
previous = ttk.Button(root,text='Previous',command=showPrevImage)
previous.grid(column=1,row=1)
nextImage = ttk.Button(root,text='Next',command=showNextImage)
nextImage.grid(column=2,row=1)
previousSet = ttk.Button(root,text='Previous Set',command=showPrevSet)
previousSet.grid(column=1,row=2)
nextSet = ttk.Button(root,text='Next Set',command=showNextSet)
nextSet.grid(column=2,row=2)
progress = ttk.Label(root,textvariable=currAll) # currAll = current/all
progress.grid(column=1,row=3)








root.mainloop()