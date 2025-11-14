import math

#finding the right camera lens


fps = 168
pixel_size = 0.00345 #in mm so it is 3.45 μm            ## G - should this not all be in a class? 
resolution_width = 1920
resolution_height = 1200
senor_size_x = 6.6 #mm
senor_size_y = 4.1 #mm
sensor_diagnol = 7.7 #mm  (we want lens to be larger than sensor diagnol)    ## G - Diagonal?
working_distance = 400 #mm
print ("Working distance is:", working_distance , "mm")


def laser_sheet(fan_angle): 
#the height of the sheet     
    alpha = math.radians(fan_angle/2) 
    y = working_distance * math.tan(alpha)
    height = 2*y                            
    print ("height of laser sheet:", height, "mm")

#the width of sheet
    beam_diameter = 2 #mm
    beam_divergence = 0.0015 #radians
    beam_y = working_distance * math.tan(beam_divergence/2)
    beam_height = 2 * beam_y + beam_diameter
    print ("width of laser sheet:", beam_height, "mm")



def AFOV(foc_len): #give in mm
#the vertical
    y = 2 * math.atan(pixel_size*resolution_height/(2*foc_len))
    VFOV = math.degrees(y)
    print ("Method 1 Vertical Field of View is:", VFOV  , "degrees")
    V = 2 * working_distance * math.tan(y/2)
    print ("Method 1 Vertical Field of View from the working distance is:" , V , "mm" )

#the horizontal     
    x = 2 * math.atan(pixel_size*resolution_width/(2*foc_len))
    HFOV = math.degrees(x)
    print ("Method 1 Horizontal Field of View is:", HFOV , "degrees")   
    H = 2 *working_distance * math.tan(x/2)
    print ("Method 1 Horizontal Field of View from the working distance is:", H , "mm")





def AFOV2(foc_len): 
    AngFOV_x = 2 *math.atan(0.5* senor_size_x / foc_len)
    print ("Method 2 Horizontal Field of View is:", math.degrees(AngFOV_x), "degrees")
    
    HFOV = working_distance*senor_size_x / foc_len
    print("Method 2 Horizontal Field of View in mm is:", HFOV, "mm")
    
    AngFOV_y =  2 *math.atan(0.5* senor_size_y / foc_len)
    print ("Method 2 Vertical Field of View is:", math.degrees(AngFOV_y), "degrees")
    
    VFOV = working_distance*senor_size_y / foc_len
    print("Method 2 Vertical Field of View in mm is:", VFOV, "mm")

    H = 2 * working_distance * math.tan(AngFOV_x/2)
    V = 2 * working_distance * math.tan(AngFOV_y/2)
    print("Method 3 Horizontal Field of View in mm is:", H , "mm")
    print("Method 3 Vertical Field of View in mm is:", V , "mm")

    

laser_sheet(45)
AFOV(8)
AFOV2(8)