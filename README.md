# Laser and Camera controller for PIV

## Control Computer Build and Setup
The control software runs on a variety of small single-board computers (SBCs).  Instructions for setup for some of the most successful are here.

- Orange Pi 5 Pro: For hardware and software installation out of the box, [see here](./SBC_Builds/OrangePi5Pro/README.md).  

After hardware and software are setup, the rest of the [steps are common](./src/README.md).  

## Software User Manual
The real-time control of the camera and laser is done by a Raspberry Pi Pico microcontroller.  Once fed its configuration, it generates the timing required for the camera and laser, and switches each on and off as needed.  It is precise and repeatable down to millisecond resolution.  

The software on the SBC that both controls the Raspberry Pi Pico and acquires the resulting images from the camera is a small Python3 program called pivexec.py.  Pivexec.py communicates to both the Pico and camera over USB.  

The sequence used by pivexec.py during a run is configured through a web page written in javascript and hosted in a Docker container.  It is called portal.js.  The end product of this configuration is to create, edit, modify and delete JSON files containing configurations.  When a configuration file is to be deployed, its name is placed in a special file named `__runfile__.deploy`.  Pivexec.py is constantly watching for this file to be created, and runs whenever it exists.  

Here is an overview of the web portal.  

![Configuration and Control](./images/PIV_Configuration_and_Control_Portal.png)