import PySpin
import numpy as np
import json
import os

dataPathRoot = '/piv/data/'

class ImageConverter:
  def __init__(self):
    pass


  def convert_image(self, image):
    """
    This function converts the image to mono 8.
    """
    processor = PySpin.ImageProcessor()
    processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)
    
    return processor.Convert(image, PySpin.PixelFormat_Mono8)

  def unconverted_raw_images(self, folder):
    files = os.listdir(folder)
    imagefiles = [f for f in files if os.path.isfile(folder+f)]
    rawimagefiles = [f for f in imagefiles if '.raw' in f]
    rawimagenames = [os.path.splitext(f)[0] for f in rawimagefiles]
    jpgimagefiles = [f for f in imagefiles if '.jpg' in f]
    jpgimagenames = [os.path.splitext(f)[0] for f in jpgimagefiles]

    rawneedsconversion = list(set(rawimagenames) - set(jpgimagenames))
    rawneedsconversion = [f+'.raw' for f in rawneedsconversion]

    return rawneedsconversion
  

  def convert_all_images(self, folder='./'):
    """
    This function converts all images in the folder to mono 8.
    """
    offline_image_width = 1440
    offline_image_height = 1080
    offline_offset_x = 0
    offline_offset_y = 0
    try:
      with open(folder + "RunSettings.json", "r") as runsettingsfile:
        runsettings = json.load(runsettingsfile)
        if 'camera' in runsettings:
          if 'Width' in runsettings['camera']:
            offline_image_width = int(runsettings['camera']['Width'])
          if 'Height' in runsettings['camera']:
            offline_image_height = int(runsettings['camera']['Height'])
    except FileNotFoundError:
      pass
    except json.JSONDecodeError:
      pass

    print(f'Using width={offline_image_width} and height={offline_image_height} in folder {folder}')
    rawneedsconversion = self.unconverted_raw_images(folder)

    try:
      for rawfilename in rawneedsconversion:
        # Load image from file into buffer
        offline_data = np.fromfile(folder + rawfilename, dtype=np.ubyte)

        # Create a new image from the buffer
        load_image = PySpin.Image.Create(offline_image_width, offline_image_height, offline_offset_x, offline_offset_y, PySpin.PixelFormat_BayerRG8, offline_data)

        image_converted = self.convert_image(load_image)
        jpgfilename = os.path.splitext(rawfilename)[0] + '.jpg'
        image_converted.Save(folder + jpgfilename)

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def convert_all_runs(self):
    files = os.listdir(dataPathRoot)
    folders = [f for f in files if os.path.isdir(dataPathRoot+f)]

    for folder in folders:
      self.convert_all_images(dataPathRoot + folder + '/')