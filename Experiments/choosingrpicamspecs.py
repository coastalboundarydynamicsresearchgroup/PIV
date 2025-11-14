import numpy as np
import matplotlib.pyplot as plt


max_macroblocks_per_second = 245760
max_macroblocks_per_frame = 8192
print ("\n","macroblocks/frame can not exceed this number:" , max_macroblocks_per_frame,"\n")   

spacing = 300  #can change this number to see the specific resolution 
desired_fps = np.linspace(1,300, spacing, True)
avaiable_macroblocks_per_frame = max_macroblocks_per_second / desired_fps

a = 3     #aspect ratio - assuming 3:2 but you can change this 
b = 2  
y = ((256*b/a)*avaiable_macroblocks_per_frame)**(1/2)
x = (y*a) / b    # aspect ratio so x would be the greater value (3:2 ratio)   
Measured_macroblocks_per_frame = (x/16) * (y/16)    #assuming 4.0 codec block for h264 files
limit = np.linspace(max_macroblocks_per_frame,max_macroblocks_per_frame,spacing)
print("Columns are as followed:")
print("fps:","\t", "resolution (C2 and C3):","\t", "macroblocks/frame:", "\n")
for i,j,k,h in zip(desired_fps,x,y,Measured_macroblocks_per_frame):
    print (i,"\t", j, "\t", k, "\t", h)


plt.plot(desired_fps, Measured_macroblocks_per_frame, label = "max avaialble macroblocks/frame")
plt.plot(desired_fps,limit, label = "limit")
plt.ylabel("Macroblocks/frame")
plt.xlabel("frames/second")
plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
plt.legend(loc="upper right")
matplotlib.pyplot.ylim(0,10000)             ## G - defined as plt??
plt.show() 

