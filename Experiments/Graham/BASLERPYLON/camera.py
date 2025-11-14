import os
import shutil
import time as t
from pypylon import pylon
import cv2




class EasyCamera:
    def __init__(self, name, fps=168, pixel_size=0.00345, resolution_width=1920, resolution_height=1200, 
                 sensor_size_x=6.6, sensor_size_y=4.1, sensor_diagonal=7.7, working_distance=400):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.name = name
        self.fps = fps   
        self.pixel_size = pixel_size  # in mm so it is 3.45 μm           
        self.resolution_width = resolution_width 
        self.resolution_height = resolution_height 
        self.sensor_size_x = sensor_size_x # mm
        self.sensor_size_y = sensor_size_y # mm
        self.sensor_diagonal = sensor_diagonal # mm  (we want lens to be larger than sensor diagonal)    
        self.working_distance = working_distance # mm
        self.images_folder = 'PythonScripts/Scripts/Graham/Images/'  # Folder to save images (make sure root is LISABER folder or change this)
        self.start_time = 0.0
        self.issues = 0
        self.timer_name = ""

    def __str__(self):
        return str("You Printed The Camera")



    # Temp Functions for testing how long processes take
    def start_stopwatch(self, timer_name = "Stopwatch"):
        self.start_time = t.time()
        self.timer_name = timer_name
        print(f"Starting Timer : {self.timer_name}")
    def check_stopwatch(self):
        run_time = t.time() - self.start_time
        print(f"{self.timer_name} has run for {run_time} seconds")
    def stop_stopwatch(self):
        run_time = t.time() - self.start_time
        print(f"{self.timer_name} ended at {run_time} seconds")
        self.start_time = 0.0
        self.timer_name = ""

    # Helper method to get next image filename based on existing files
    def _get_next_image_filename(self):
        # Ensure the images folder exists
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

        # List all files in the folder
        files = os.listdir(self.images_folder)

        # Filter and extract the highest number from 'imageX.jpg'
        image_files = [f for f in files if f.startswith('image') and f.endswith('.jpg')]
        numbers = [int(f[5:-4]) for f in image_files]  # Get the numbers from filenames
        
        next_number = max(numbers) + 1 if numbers else 1  # Determine next number
        return f'image{next_number}.jpg'

    # Takes a photo and saves it to the images folder
    def take_photo(self, timeout = 2000):
        # Start grabbing the image
        self.camera.StartGrabbing()
        with self.camera.RetrieveResult(timeout) as result:  # timeout is in ms
            if result.GrabSucceeded():
                # Convert the image to RGB format
                converter = pylon.ImageFormatConverter()
                converter.OutputPixelFormat = pylon.PixelType_RGB8packed
                image = converter.Convert(result).GetArray()

                # Get the next image filename
                image_filename = self._get_next_image_filename()
                image_path = os.path.join(self.images_folder, image_filename)

                # Save the image using OpenCV
                cv2.imwrite(image_path, image)
                print(f"Image saved as {image_path}")
            else:
                print("Failed to grab image.")
                self.issues += 1

        self.camera.StopGrabbing()

    # Takes multiple photos with a delay in between
    def take_photos(self, count, time_between, delay=0, timeout = 2000):
        print(f"Waiting {delay} seconds before starting...")
        t.sleep(delay)  # Delay before taking photos



        for i in range(count):
            print(f"Taking photo {i + 1}/{count}...")
            self.take_photo(timeout = timeout)
            t.sleep(time_between)  # Wait between taking photos

    # Clears the images folder
    def clear_folder(self):
        if os.path.exists(self.images_folder):
            shutil.rmtree(self.images_folder)  # Remove folder and its contents
            os.makedirs(self.images_folder)  # Recreate empty folder
            print("Folder cleared.")
        else:
            os.makedirs(self.images_folder)  # Create the folder if it doesn't exist
            print("Folder created.")

# Example usage
if __name__ == "__main__":
    camera = EasyCamera("My Camera")




    camera.clear_folder()
    camera.take_photos(count=5, time_between=1, delay=1)
    print(f"Camera encountered {camera.issues} Errors")