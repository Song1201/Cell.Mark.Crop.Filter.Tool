'''
Rules for making marks:


Rules for dealing with marks:
For the cells that are close to the border, we moved the image, which leads to the cells are
not in the center of images anymore. Considering the rotation we are going to do later and the 
fact that for image classification we don't ask for the object in the center of image, we
empirically say that having images in which cells are not in the center will not have negetive 
influence on the network.
For the cells that are stick together, we capture them without any adjustment. We think this 
will reflect the assembling of the cells.
'''

import numpy as np
import os
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt
from scipy import signal
#%%
r = 50  # half height and half width
setLeng = 15 # the number of the images in one set
imageFold = 'C:/DeepMAC/OralScanLowNr36'
tarImFold = 'C:/DeepMAC/OralScanLowNr36Crop'
#tarImFront = tarImFold+'/cell1_'
imHeig = 1024 # image height
imWid = 1344 # image width
# Create the laplacian operator Kernel
lapKer = ImageFilter.Kernel(size=(3,3),kernel=(0,1,0,1,-4,1,0,1,0)) 
lapKer = np.array([[0,1,0],[1,-4,1],[0,1,0]]) # laplacian kernel
tarSetLeng = 5 # target set length

# Process each coordinate file one by one
for coorFile in os.listdir(imageFold):
    if coorFile.endswith('.dat'):   
        print('Processing:'+coorFile)
        coor = np.load(imageFold+'/'+coorFile) # coor = Coordinate
        # the variance of the result of convolve with the laplacian kernel
        lapVars = np.empty([coor.shape[0],setLeng])   
        # move the mark points away from the border if it is too close to the border
        for row in range(coor.shape[0]): 
            if coor[row,0] < r:
                coor[row,0] = r
            if coor[row,1] < r:
                coor[row,1] = r
            if coor[row,0] > imWid - r - 1:
                coor[row,0] = imWid - r - 1
            if coor[row,1] > imHeig - r - 1:
                coor[row,1] = imHeig - r - 1
                
        # Process each image in the image set one by one
        for imageNr in range(setLeng): # imageNr is iamge number
            # for whose image number is 1 digit, add a 0 to make it the same to the filename
            if imageNr < 10:
                imageFile = imageFold + '/' + coorFile[0:-4] + '_00' + str(imageNr) + '.tif'                    
            else:
                imageFile = imageFold + '/' + coorFile[0:-4] + '_0' + str(imageNr) + '.tif'
            
            allCell = Image.open(imageFile)
            allCell = np.array(allCell.getdata()).reshape(imHeig,imWid)
            for row in range(coor.shape[0]):
                xMark = coor[row,0]
                yMark = coor[row,1]
                oneCell = allCell[(yMark-r):(yMark+r),(xMark-r):(xMark+r)]
                # the result after convolve with laplacian kernel
                covLap = np.abs(signal.convolve2d(oneCell,lapKer,mode='valid')) 
                # calculate the variance divided by the number of elements
                lapVar = np.var(covLap) 
                lapVars[row,imageNr] = lapVar

        bestFocus = np.argmax(lapVars,axis=1) # the image number which has the best focus
        for markNr in range(bestFocus.shape[0]):
            # markNr is mark number
            if bestFocus[markNr] < int(tarSetLeng/2):
                bestFocus[markNr] = int(tarSetLeng/2)
            if bestFocus[markNr] > setLeng - int(tarSetLeng/2) - 1:
                bestFocus[markNr] = setLeng - int(tarSetLeng/2) - 1
        # image which has been selected to create single cell
        imSel = bestFocus.reshape((bestFocus.shape[0],1)).repeat(tarSetLeng,axis=1)
        # bias matrix to add to imSel, in order to build a matrix which every row corresponding
        # to a mark and every element corresponding to the selected image number for this mark.
        biasMat = np.arange(-int(tarSetLeng/2),int(tarSetLeng/2)+1).reshape((1,tarSetLeng))\
        .repeat(bestFocus.shape[0],0)
        imSel = imSel + biasMat
        for imageNr in range(setLeng):
            searRes = np.argwhere(imSel == imageNr) # search result
            if searRes.shape[0] != 0:
                if imageNr < 10:
                    imageFile = imageFold + '/' + coorFile[0:-4] + '_00' + str(imageNr) + '.tif'                    
                else:
                    imageFile = imageFold + '/' + coorFile[0:-4] + '_0' + str(imageNr) + '.tif'
            
                allCell = Image.open(imageFile)
                for oneRes in searRes:
                    xMark = coor[oneRes[0],0]
                    yMark = coor[oneRes[0],1]
                    box = (xMark-r,yMark-r,xMark+r,yMark+r)
                    oneCell = allCell.crop(box)
                    # target image file
                    tarImFile = tarImFold+'/'+coorFile[0:-4]+'_'+str(oneRes[0])+'_'+\
                    str(imageNr)+'.tif'
                    oneCell.save(tarImFile)
                
                
            
                
                
                
                
            
            
            
 
    
        
        
        

        

        


#a = np.load('C:/DeepMAC/OralScanNr1/glas1_1_000.dat')
#b = np.load('C:/DeepMAC/OralScanNr1/glas1_1_001.dat')
#c = np.load('C:/DeepMAC/OralScanNr1/glas1_1_002.dat')