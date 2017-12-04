# Installed Packages Arch ARM
- create_ap 
- htop 
- sudo
- vim
- git
- python3 (3.6.2)

# Serial Port Setup
- add `enable_uart=1`
- `/boot/cmdline.txt #remove console=ttyAMA0,115200 kgdboc=ttyAMA0,115200`
- stop service serial-getty@ttyS0.service
- disable service serial-getty@ttyS0.service

# Activated Services
wifi_ap
