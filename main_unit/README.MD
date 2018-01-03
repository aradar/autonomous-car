# Installed Packages Arch ARM
- create_ap 
- htop 
- sudo
- vim
- git
- python3 (3.6.2)
- cmake, make, gcc, boost (,libusb.dev)
- pixy library

# Serial Port Setup
- add `enable_uart=1`
- `/boot/cmdline.txt #remove console=ttyAMA0,115200 kgdboc=ttyAMA0,115200`
- stop service serial-getty@ttyS0.service
- disable service serial-getty@ttyS0.service

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

# Activated Services
wifi_ap
