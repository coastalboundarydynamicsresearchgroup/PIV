from filewatcher import RunState
from camera import Camera

with Camera(RunState()) as cam:
    print(cam.caminfo)
    cam.framerate = 1000
    cam.configure_chunk_timestamp()
    cam.start_acquisition_mode()
    #cam.configure_soft_trigger()

    # Capture a single image
    #cam.trigger_software()
    cam.acquire_image(convert=True)

    cam.end_acquisition_mode()
    print(f'cam.status: {cam.status}')

