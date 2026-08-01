# Particle Image Velocimetry Controller Software setup

## Build and Flash the Raspberry Pi Pico Firmware
- In VSCode, install the Raspberry Pi Pico extension.
- Using a console: `$ sudo apt update` and `$ sudo apt install build-essential gdb`.
- Assuming you have cloned the git PIV repository into ~/github/PIV, open VSCode and open folder `~/github/PIV/src/pico/piv`.  The Pico

## Generic Steps to Build Docker Containers
Some of the components of the PIV controller run in docker containers, and the first step in software setup is to build these containers.  
There are scripts for these components, which do the majority of the setup work, but the `npm install` step sometimes fails during the build and must be done manually later:
- `./dockb`       # Build the 1.0 version of the container  
- `./dock-start`  # Launch a console in the (possibly) partially-built container  
- `npm start`     # Attempt to run the component inside the container, if it fails then:  
- `npm install`   # Redo the failed step  
- `npm start`     # Rerun the component inside the container, confirm it works now  

When the 1.0 version is working, the running container must be committed as the 1.1 version, which will be what runs in production.  On a new console:  
`docker container ls` to obtain the container ID, then `docker container commit <container ID> louisross/<component>:1.1`:

![Docker Container Commit for the Portal component](./docker_container_commit.png)

From this point, the 1.0 version is considered deprecated, and only the 1.1 version will be run.  The `./dock` command will run the 1.1 version in a console for debugging.

## Build the `portal` Component
The PIV code is assumed to have been cloned from the github repositry into a folder called `~/github`.  Thus, the `portal` component is in `~/github/PIV/src/portal`.

Execute the generic steps above in the `~/github/PIV/src/portal` directory, commiting the 1.1 version as `louisross/portal:1.1`.

## Build the `pivdeploy` Component
The PIV code is assumed to have been cloned from the github repository into a folder called `~/github`.  Thus, the `pivdeploy` component is in `~/github/PIV/src/pivdeploy`.

Execute the generic steps above in the `~/github/PIV/src/pivdeploy` directory, commiting the 1.1 version as `louisross/piv-deploy:1.1`.

## Install Dependencies for pivexec Component
`$ python -m pip install --user watchdog pyserial requests`

`$ mkdir /pivdata/data`  
`$ mkdir /pivdata/configuration`  

## Setup Acquisition Software to Start Automatically on Boot
The PIV data acquisition software is in three subsystems:
- `portal`      A Single-Page Application (SPA) web page written in Javascript using the React.js framework
- `pivdeploy`   A web service for file management and deployment control written in Javascript using the Node.js framework
- `pivexec`     A Python application to do the low-level real-time communication and control as configured

The two web services, `portal` and `pivdeploy`, run inside Docker containers that act to keep the isolated from each other and other components in the system.  The real-time Python application, `pivexec`, needs access to the hardware of the host system, so runs in the host.

The whole system can be run manually:  
`> cd /home/piv/github/PIV/src`  
`> docker compose up`  
`> cd pivexec`  
`> python3 ./pivexec.py`  

In order to automate this sequence, these commands are summarized in two service files in `/home/piv/github/PIV/bootfiles`:  
`docker-compose-piv.service`   
`pivexecute.service`

To enable these files to start services automatically, first copy them to `/etc/systemd/system`, then enable them as services.:  
- `> cp /home/piv/github/PIV/bootfiles/docker-compose-piv.service /etc/systemd/system`  
- `> sudo systemctl enable docker-compose-piv.service`  
- `> cp /home/piv/github/PIV/bootfiles/pivexecute.service /etc/systemd/system`  
- `> sudo systemctl enable pivexecute.service`  

For test, also start them manually:  
- `> sudo systemctl start docker-compose-piv.service`  
- `> sudo systemctl start pivexecute.service`  

The whole acquisition system, including the SPA web page and laser/camera control, should now be running.  You should be able to confirm by connecting with a web browser.

Another good confirmation is to type:  
`> docker ps`  
`CONTAINER ID   IMAGE                      COMMAND                  CREATED       STATUS       PORTS                                         NAMES`  
`846a5e9cb83a   louisross/portal:1.1       "docker-entrypoint.s…"   4 hours ago   Up 4 hours   0.0.0.0:80->3000/tcp, [::]:80->3000/tcp       piv-portal`  
`e47b2907a614   louisross/piv-deploy:1.1   "npm start"              4 hours ago   Up 4 hours   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   piv-deploy`  

The output from this command shows what docker contaiers are currently running.  The two images `louisross/portal:1.1` and `louisross/piv-deploy:1.1` indicate that the web servcies are running.


