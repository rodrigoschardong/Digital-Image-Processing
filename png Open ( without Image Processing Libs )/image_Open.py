"""
    author: Rodrigo Schardong
    entity: UERGS - Universidade Estadual do Rio Grande do Sul
"""

#https://www.w3.org/TR/PNG/#8Interlace

#Libs to read file
import zlib
import numpy as np

#Libs Just to Display image and interact with them
from matplotlib import pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

"""
    Function name: PutInAByte
    Input: pixel value
    output: pixel value between 0 and 255
    Doesn't required any library
"""
def PutInAByte(byte):
    if(byte >= 256):
        byte -= 256
    return byte

"""
    Function name: PNG_OPEN
    Input: image file name
    output: image 3D array [height, width, channels]
    Required libraries: zlib, numpy
"""
def PNG_Open(image_name):
    #reading file's bytes
    with open(image_name, 'rb') as i:
        image_b = i.read(-1)
    
    #Getting file's info
    pngLenght = len(image_b)
    pngSignature = image_b[:8]    
    
    #Getting the first chunk
    dataFromChunks = []
    crcLenght = 4
    index = 8
    
    chunkLength = int.from_bytes(image_b[index: index + 4], "big") 
    index += 4
    chunkType = image_b[index: index + 4].decode("utf-8")
    index += 4
    chunkData = image_b[index : index + chunkLength]
    index += chunkLength
    index += crcLenght
    
    #Getting data from first chunk
    width = int.from_bytes(chunkData[0:4], "big")  
    height = int.from_bytes(chunkData[4:8], "big")  
    bitDepth = chunkData[8]
    colourType = chunkData[9] 
    compressionMethod = chunkData[10]
    filterMethod = chunkData[11] 
    interlaceMethode = chunkData[12] 
    #print("Largura: ", width)
    #print("Altura: ", height)
    
    #Collecting compressed data
    while(index <= pngLenght):
        chunkLength = int.from_bytes(image_b[index: index + 4], "big") 
        index += 4
        chunkType = image_b[index: index + 4].decode("utf-8")
        index += 4
        chunkData = image_b[index : index + chunkLength]
        index += chunkLength
        index += crcLenght
        if(chunkType == "IDAT"):
            dataFromChunks.append(chunkData)
    
    #print("dataFromChunks: ", dataFromChunks)
    #print("dataFromChunks lenght: ", len(dataFromChunks[0]))
    
    #decompressing data
    decompressPixels = zlib.decompress(dataFromChunks[0])
    #print("Tamanho da Imagem: ", len(decompressPixels))
    #print("Imagem: ", decompressPixels)
    
    #creating images channels
    out = np.zeros((height, width, 3)) # 3 channel R, G and B
    
    #Filling the channels 
    index = 0
    for y in range (0, height):
        #Getting the filter
        filterType = decompressPixels[index]
        index +=1     
        
        for x in range (0, width):
            if(filterType == 1):
                if(x == 0): 
                    out[y, x, 0] = decompressPixels[index]
                    out[y, x, 1] = decompressPixels[index + 1]
                    out[y, x, 2] = decompressPixels[index + 2]
                else:
                    out[y, x, 0] = PutInAByte(decompressPixels[index] + out[y, x - 1, 0])
                    out[y, x, 1] = PutInAByte(decompressPixels[index + 1] + out[y, x - 1, 1])
                    out[y, x, 2] = PutInAByte(decompressPixels[index + 2] + out[y, x - 1, 2])   
                    
            elif(filterType == 2):
                out[y, x, 0] = PutInAByte(decompressPixels[index] + out[y- 1, x, 0])
                out[y, x, 1] = PutInAByte(decompressPixels[index + 1] + out[y- 1, x, 1])
                out[y, x, 2] = PutInAByte(decompressPixels[index + 2] + out[y- 1, x, 2])
                
            elif(filterType == 0):
                out[y, x, 0] = PutInAByte(decompressPixels[index])
                out[y, x, 1] = PutInAByte(decompressPixels[index + 1])
                out[y, x, 2] = PutInAByte(decompressPixels[index + 2])
            else:
                print("Filter type: ", filterType)
            index += 3
    return out


#Open Png file, display it and show pixels values of each channel from choosen position
def main(image_name, x, y):
    image = PNG_Open(image_name)
    
    print("O pixel vermelho na posicao (", x, ", ", y, ") possui valor: ", image[y, x, 0].astype(int))
    print("O pixel verde na posicao (", x, ", ", y, ") possui valor: ", image[y, x, 1].astype(int))
    print("O pixel azul na posicao (", x, ", ", y, ") possui valor: ", image[y, x, 2].astype(int))
    
    if(image[y, x, 0] + image[y, x, 1] + image[y, x, 2] > (256 * 1.5)):
        image[y, x, 0] = 0
        image[y, x, 1] = 0
        image[y, x, 2] = 0
    else:
        image[y, x, 0] = 255
        image[y, x, 1] = 255
        image[y, x, 2] = 255
    
    plt.imshow(image.astype(int))
    plt.plot()