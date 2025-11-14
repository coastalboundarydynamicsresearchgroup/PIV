import PySpin
import numpy as np
import sys


class Camera:
  def __init__(self):
    self.cam = None
    self.caminfo = {}
    self.cam_list = None
    self.cam_list_size = 0
    self.system = None
    self.imagenumber = 0
    self.exposure_time_us = 0

    self.status = ""
    self.valid = False
    
  def __enter__(self):
    self.system = PySpin.System.GetInstance()
    self.cam_list = self.system.GetCameras()
    self.cam_list_size = self.cam_list.GetSize()

    if self.cam_list_size == 0:
      self.status = "No camera detected"
      self.valid = False
    else:
      self.cam = self.cam_list[0]
      self.load_device_info()
      if self.valid:
        self.cam.Init()
        self.caminfo['MaxWidth'] = self.cam.WidthMax.GetValue()
        self.caminfo['MaxHeight'] = self.cam.HeightMax.GetValue()
        self.caminfo['Width'] = self.cam.Width.GetValue()
        self.caminfo['Height'] = self.cam.Height.GetValue()

        self.status = "Camera initialized"
        self.valid = True

    return self


  def __exit__(self, *args):
    self.close()

  def close(self):
    if self.cam is not None:
      self.reset_trigger()
      self.reset_exposure()
      self.cam.DeInit()
      del self.cam
      self.cam = None
    if self.cam_list is not None:
      self.cam_list.Clear()
      del self.cam_list
      self.cam_list = None
    if self.system is not None:
      self.system.ReleaseInstance()
      del self.system
      self.system = None

  def load_device_info(self):
    """
    This function loads the device information of the camera from the transport
    layer; please see NodeMapInfo example for more in-depth comments on printing
    device information from the nodemap.
    """

    try:
      nodemap = self.cam.GetTLDeviceNodeMap()
      node_device_information = PySpin.CCategoryPtr(nodemap.GetNode('DeviceInformation'))

      if PySpin.IsReadable(node_device_information):
        features = node_device_information.GetFeatures()
        for feature in features:
          node_feature = PySpin.CValuePtr(feature)
          if PySpin.IsReadable(node_feature):
            self.caminfo[node_feature.GetName()] = node_feature.ToString()
          else:
            self.caminfo[node_feature.GetName()] = 'Node not readable'

      self.status = "Camera information loaded"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = str(ex)
      self.valid = False


  def configure_trigger(self):
    """
    This function configures the camera trigger mode.
    """
    try:
      if self.cam.TriggerMode.GetAccessMode() != PySpin.RW:
        self.status = "Trigger mode not available"
        self.valid = False
        return
      if self.cam.TriggerSelector.GetAccessMode() != PySpin.RW:
        self.status = "Trigger selector not available"
        self.valid = False
        return
      if self.cam.TriggerSource.GetAccessMode() != PySpin.RW:
        self.status = "Trigger source not available"
        self.valid = False
        return

      self.cam.TriggerMode.SetValue(PySpin.TriggerMode_Off)
      self.cam.TriggerSelector.SetValue(PySpin.TriggerSelector_FrameStart)
      self.cam.TriggerSource.SetValue(PySpin.TriggerSource_Line0)
      self.cam.TriggerMode.SetValue(PySpin.TriggerMode_On)
      self.status = "Trigger mode set to frame start on line 0"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return

  def reset_trigger(self):
    """
    This function resets the camera trigger mode to continuous.
    """
    try:
      if self.cam.TriggerMode.GetAccessMode() != PySpin.RW:
        self.status = "Trigger mode not available"
        self.valid = False
        return

      self.cam.TriggerMode.SetValue(PySpin.TriggerMode_Off)
      self.status = "Trigger mode set to continuous"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def configure_black_level(self, black_level):
    """
    This function configures the camera black level, as specified in percnet.
    """
    try:
      if self.cam.BlackLevelSelector.GetAccessMode() != PySpin.RW:
        self.status = "Black level mode not available"
        self.valid = False
        return
      self.cam.BlackLevelSelector.SetValue(PySpin.BlackLevelSelector_All)

      if self.cam.BlackLevel.GetAccessMode() != PySpin.RW:
        self.status = "Black level not available"
        self.valid = False
        return
      self.cam.BlackLevel.SetValue(black_level)
      self.status = f'Black level set to {black_level}'
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return

  def reset_black_level(self):
    """
    This function resets the camera black level to off.
    """
    try:
      if self.cam.BlackLevelSelector.GetAccessMode() != PySpin.RW:
        self.status = "Black level mode not available"
        self.valid = False
        return

      self.cam.BlackLevelSelector.SetValue(PySpin.BlackLevelAuto_Off)
      self.status = "Black level mode set to off"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return

  def configure_exposure(self, exposure_time):
    """
    This function configures the camera exposure time, as specified in ms.
    """
    try:
      if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
        self.status = "Exposure mode not available"
        self.valid = False
        return
      self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)

      if self.cam.ExposureTime.GetAccessMode() != PySpin.RW:
        self.status = "Exposure time not available"
        self.valid = False
        return
      self.exposure_time_us = exposure_time * 1000.0
      self.exposure_time_us = min(self.cam.ExposureTime.GetMax(), self.exposure_time_us)
      self.cam.ExposureTime.SetValue(self.exposure_time_us)
      self.status = f'Exposure time set to {self.exposure_time_us} us'
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return

  def reset_exposure(self):
    """
    This function resets the camera exposure time to auto.
    """
    try:
      if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
        self.status = "Exposure mode not available"
        self.valid = False
        return

      self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Continuous)
      self.status = "Exposure mode set to continuous"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return

  def configure_gain(self, gain):
    """
    This function configures the camera gain, as specified in db (0-47 db).
    """
    try:
      if self.cam.GainAuto.GetAccessMode() != PySpin.RW:
        self.status = "Gain mode not available"
        self.valid = False
        return
      self.cam.GainAuto.SetValue(PySpin.GainAuto_Off)

      if self.cam.Gain.GetAccessMode() != PySpin.RW:
        self.status = "Gain not available"
        self.valid = False
        return
      self.cam.Gain.SetValue(gain)
      self.status = f'Gain set to {gain}'
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return

  def reset_gain(self):
    """
    This function resets the camera gain to auto.
    """
    try:
      if self.cam.GainAuto.GetAccessMode() != PySpin.RW:
        self.status = "Gain mode not available"
        self.valid = False
        return

      self.cam.GainAuto.SetValue(PySpin.GainAuto_Continuous)
      self.status = "Gain mode set to auto continuous"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def configure_gamma(self, gamma):
    """
    This function configures the camera gamma, as specified as the exponent for each pixel, typically 0.5-2.0.
    """
    try:
      if self.cam.GammaEnable.GetAccessMode() != PySpin.RW:
        self.status = "Gamma mode not available"
        self.valid = False
        return
      self.cam.GammaEnable.SetValue(True)

      if self.cam.Gamma.GetAccessMode() != PySpin.RW:
        self.status = "Gamma not available"
        self.valid = False
        return
      self.cam.Gamma.SetValue(gamma)
      self.status = f'Gamma set to {gamma}'
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def reset_gamma(self):
    """
    This function resets the camera gamma to auto.
    """
    try:
      if self.cam.GammaEnable.GetAccessMode() != PySpin.RW:
        self.status = "Gamma mode not available"
        self.valid = False
        return

      self.cam.GammaEnable.SetValue(False)
      self.status = "Gamma mode set to off"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def start_acquisition_mode(self):
    """
    This function starts the camera acquisition.
    """
    try:
      if self.cam.AcquisitionMode.GetAccessMode() != PySpin.RW:
        self.status = "Acquisition mode not available"
        self.valid = False
        return

      self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
      self.cam.BeginAcquisition()

      self.status = "Acquisition started"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def end_acquisition_mode(self):
    """
    This function ends the camera acquisition.
    """
    try:
      self.cam.EndAcquisition()
      self.status = "Acquisition ended"
      self.valid = True

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return


  def acquire_image(self, folder='./'):
    """
    This function acquires and saves 10 images from a device.
    Please see Acquisition example for more in-depth comments on acquiring images.
    """

    try:
      result = True

      #  Retrieve next received image
      image_result = self.cam.GetNextImage(10)

      #  Ensure image completion
      if image_result.IsIncomplete():
        self.status = f'Image incomplete with image status {image_result.GetImageStatus()}'
        self.valid = False

      else:
        # Create a unique filename, save image to file.
        filename = f'Trigger-{self.caminfo["DeviceSerialNumber"]}-{self.imagenumber}.raw'
        image_result.Save(folder + filename)

        #image_converted = self.convert_image(image_result)
        #filename = f'Trigger-{self.caminfo["DeviceSerialNumber"]}-{self.imagenumber}.jpg'
        #image_converted.Save(folder + filename)

        image_result.Release()
        self.imagenumber += 1

    except PySpin.SpinnakerException as ex:
      result = False

    return result


  def convert_image(self, image):
    """
    This function converts the image to mono 8.
    """
    processor = PySpin.ImageProcessor()
    processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)
    
    return processor.Convert(image, PySpin.PixelFormat_Mono8)


  def convert_all_images(self, folder='./'):
    """
    This function converts all images in the folder to mono 8.
    """
    offline_image_width = 1440
    offline_image_height = 1080
    offline_offset_x = 0
    offline_offset_y = 0

    try:
      for i in range(self.imagenumber):
        filename = f'Trigger-{self.caminfo["DeviceSerialNumber"]}-{i}.raw'

        # Load image from file into buffer
        offline_data = np.fromfile(folder + filename, dtype=np.ubyte)

        # Create a new image from the buffer
        load_image = PySpin.Image.Create(offline_image_width, offline_image_height, offline_offset_x, offline_offset_y, PySpin.PixelFormat_BayerRG8, offline_data)

        image_converted = self.convert_image(load_image)
        filename = f'Trigger-{self.caminfo["DeviceSerialNumber"]}-{i}.jpg'
        image_converted.Save(folder + filename)
        load_image.Release()

    except PySpin.SpinnakerException as ex:
      self.status = f'Error: {ex}'
      self.valid = False

    return