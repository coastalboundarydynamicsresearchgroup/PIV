import os
import glob
import numpy as np

import PySpin

import glob

data_path = "/pivdata/data"

# TODO get this from user
epoch = "Sample"

# Find all .raw files in the directory
raw_files = glob.glob(os.path.join(data_path, epoch, "*.raw"))

for raw_file in raw_files:
    file_name = os.path.basename(raw_file)

    # Assuming 'raw_image.raw' is your raw file and you know its format
    # You might need to specify the pixel format and dimensions if the file format doesn't inherently provide them.
    # For example, if it's a raw BayerRG8 image with a known width and height:
    # image = PySpin.Image.Create(width, height, 0, 0, PySpin.PixelFormat_BayerRG8, raw_data_buffer)
    # Or, if Spinnaker can interpret the raw file directly:
    # image = PySpin.Image.Load(raw_file, PySpin.SPINNAKER_IMAGE_FILE_FORMAT_FROM_FILE_EXT)
    #image = PySpin.Image.Create(1440, 1080, 0, 0, PySpin.PixelFormat_BayerRG8, raw_data_buffer)

    #processor = PySpin.ImageProcessor.GetInstance()
    # Set the desired output format for conversion
    #processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR) # High-quality debayering
    #converted_image = processor.Convert(image, PySpin.PixelFormat_BGR8)


    #converted_image.Save(os.path.join(data_path, epoch, file_name + ".jpg"), PySpin.ImageFileFormat_JPEG)

    # Load image from file into buffer
    offline_data = np.fromfile(raw_file, dtype=np.ubyte)

    # Create a new image from the buffer
    load_image = PySpin.Image.Create(1440, 1080, 0, 0, PySpin.PixelFormat_BayerRG8, offline_data)

    processor = PySpin.ImageProcessor()
    processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)
    
    image_converted = processor.Convert(load_image, PySpin.PixelFormat_Mono8)

    jpg_filepath = os.path.join(data_path, epoch, file_name + ".jpg")
    image_converted.Save(jpg_filepath)
    #load_image.Release()

