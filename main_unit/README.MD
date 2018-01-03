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

## Add user to sudoers file
- `sudoedit /etc/sudoers`
- add `alarm ALL=(ALL) ALL`

## Serial Port Setup
- add `enable_uart=1`
- `/boot/cmdline.txt #remove console=ttyAMA0,115200 kgdboc=ttyAMA0,115200`
- stop service serial-getty@ttyS0.service
- disable service serial-getty@ttyS0.service

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

