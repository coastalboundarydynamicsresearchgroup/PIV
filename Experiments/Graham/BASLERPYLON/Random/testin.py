from pypylon import pylon
import cv2

# Create an instant camera object with the camera device found first
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Start the camera
camera.StartGrabbing()

# Create an image converter to convert the raw image to a format usable by OpenCV
converter = pylon.ImageFormatConverter()

# Convert to RGB (OpenCV works with BGR, but RGB works here too)
converter.OutputPixelFormat = pylon.PixelType_RGB8packed

# Wait for the first image to be grabbed
with camera.RetrieveResult(2000) as result:  # 2000 ms timeout
    if result.GrabSucceeded():
        # Convert the image to a format usable by OpenCV
        image = converter.Convert(result).GetArray()

        # Save the image using OpenCV
        cv2.imwrite('PythonScripts/Scripts/Graham Testing/Images/captured_image.jpg', image)

    else:
        print("Failed to grab image.")

# Stop grabbing and close the camera
camera.StopGrabbing()