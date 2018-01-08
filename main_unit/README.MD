# PI setup
## Installed Packages Arch ARM
- boost
- cmake
- create_ap
- fish
- gcc
- git
- htop
- vim
- sudo
- make
- python2
- python3
- pkg-config
- python-virtualenvwrapper
- fakeroot

## Install custom dependencies
- go to the `main_unit/dependencies` dir and install all dependencies which are located there
- example installation of the libpixyusb library
  - go into the `libpixyusb` dir 
  - call `makepkg -sic`
  - confirm the installation

## Add user to sudoers file
- `sudoedit /etc/sudoers`
- add `alarm ALL=(ALL) ALL`

## Serial Port Setup
- open `/boot/confix.txt`
- add `enable_uart=1`
- open `/boot/cmdline.txt`
- remove `console=ttyAMA0,115200`
- remove `kgdboc=ttyAMA0,115200`
- disable getty service on ttyS0 `systemctl disable serial-getty@ttyS0.service`
- stop getty service on ttyS0 `systemctl stop serial-getty@ttyS0.service`
- add user to the `uucp` group with `usermod -G uucp alarm` to prevent the requirement of su rights to use the serial port

## Activating hotspot
- clone the repo
- copy main_unit/systemd-units/wifi_ap.service to `/etc/systemd/system/`
- change the ssid and password entries in `/etc/create_ap.conf` 
- activate the service with `systemctl enable wifi_ap`
- start the service directly with `systemctl start wifi_ap`

## Activated Services
- wifi_ap

## Setup virtualenvwrapper for bash
- open `~/.bashrc`
- add `export WORKON_HOME=~/.virtualenvs`
- add `source /usr/bin/virtualenvwrapper.sh`
- create the venv with `mkvirtualenv main_unit`

# Setup python dev environment
- install and setup a python venv environment
  - bash <http://virtualenvwrapper.readthedocs.io/en/latest/>
  - fish <https://github.com/adambrenecki/virtualfish>
  - windows (cmd) <https://pypi.python.org/pypi/virtualenvwrapper-win>
  - raw venv through python3 or one of the many other venv environments
  - a good explanation what a virtual env does and how you can set it up can be found here
    <https://wiki.archlinux.org/index.php/Python/Virtual_environment>
- activate your venv (how this works depends on your venv environment)
- install the dependencies
  - go into the folder with the `requirements.txt` file and call `pip install -r requirements.txt`
- install the ai_robo_car python library in dev mode
  - go into the folder with the `setup.py` file and call `pip install -e .`

## Setup Pixy Cam (Arch Way)

 - NOTE: if you are using an ubuntu-based distribution, please try to follow the guideline on the official developer [wiki](http://cmucam.org/projects/cmucam5/wiki)
 - clone git repository of pixycam: https://github.com/charmedlabs/pixy.git
 - [install custom dependencies](#install-custom-dependencies)
 - execute bash script `build_libpixyusb_swig.sh` in pixy's home `scripts/`
 - go to `../src/host/linux/` and export pixy rules as following: `sudo cp pixy.rules /etc/udev/rules.d/` to use Pixy Cam as non-root user
 - change in pixy's home to `build/libpixyusb_swig` and try to execute `python2 get_blocks.py`
 - if the script is throwing an exception try to format `get_blocks.py` to python3 syntax by changing the `print'...'` lines to `print(...)`and try again for python3
 - now you should see an output or at least no more exceptions
### Setup PixyMon
 - to set a signature by not using the teach mode of the Pixy Cam you have to set up PixyMon
 - make sure you have installed at least `qt4` in addition to the other dependencies above
 - change to pixy's home `scripts/` and run `./build_pixymon_src.sh`
 - change to `../build/pixymon/bin/`
 - and run `./PixyMon`

### Known Issues (Pixy Cam)
 - `scripts/build_libpixyusb_swig.sh` is throwing several exceptions
	 - try to update your `gcc`
	 - script successfully built by using `gcc 7.2.1` 
 - Using **Anaconda** as virtual environment:
	 - `gcc` in anaconda is very... very outdated at the moment
	 - if you still want to use Anaconda try a conda-forge: `conda create -n your_enironment_name python=3.6 numpy cython pystan -c conda-forge`
	 - perhaps you have to reboot
 - `get_blocks.py` cannot import the pixy module
	 - try to run `pip install -e .` in the same directory as `get_blocks.py`
	 - make sure to activate your virtual environment by doing the step named above
