# PIV Controller using Orange Pi 3 Pro

## Boot the OrangePi
- Burn the file `Orangepi5pro_1.0.6_ubuntu_jammy_desktop_xfce_linux6.1.43.img` into a micro SD card using BalenaEtcher or similar.  The card should be at least 32 GB.
- Insert the SD card into the SBC, plus monitor, keyboard, mouse.  Power up with USB C supply.  The SBC should boot within about 10 seconds, without pressing the power button.
- When logged in (default user os orangepi), create the `piv` user on a console with
```
$ sudo adduser piv
[sudo] password for orangepi: orangepi
. . .
New password: piv
```
- Add user `piv` to the sudo group: `$ sudo adduser piv sudo`
- Change the default login at startup to the `piv` user: `$ sudo auto_login_cli.sh piv`

- Log out of user `orangepi` and log in to user `piv`.  This will be the working directory from now on.

## Install software
- **Visual Studio Code**
  - Go to the Visual Studio Code download page and download the .deb file for Arm64.
  - In a console, `$ cd ~/Downloads` and install the local package with `$ sudo apt install [file name starting with code_].deb`.
  - After the installation starts, watch for popups asking for permission to access repositories, and grant permission.
- **The piv controller repository**
  - In a console, `$ mkdir github` and `$ cd github`.
  - Clone the repository with `$ git clone https://github.com/coastalboundarydynamicsresearchgroup/PIV.git`.
- **FLIR software (Spinnaker SDK, SpinView)**
  - [Where to get the files from?]  Obtain the file `spinnaker-4.2.0.46-arm64-22.04-pkg.tar.gz`.  Extract its contents, then `$ cd spinnaker-4.2.0.46-arm64`.
  - Follow the instructions in the READM.md file for Ubuntu 22.04.  This should boil down to two steps:
    1. `$ sudo apt-get install libusb-1.0-0 qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools`
    2. `sudo sh install_spinnaker_arm.sh`

    The second script will install the whole spinnaker package, asking for permission to install various options.  Take the default 'Y' answer for all but the last question about a giga camera.

- **FLIR Python toolkit**
  - [Where to get the file from?]  Obtain the file `spinnaker_python-4.2.0.46-cp310-cp310-linux_aarch64-22.04.tar.gz`.  Extract its contents, then `$ cd spinnaker_python-4.2.0.46-cp310-cp310-linux_aarch64-22.04`.
  - Follow the instructions in the README.md file for Ubuntu 22.04.  **Be sure to run `sudo apt update` before executing the instructions**.
- **Docker**
  This image of Ubuntu 22.04 comes with Docker pre-installed, so no action is needed here.

  
