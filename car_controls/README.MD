# Car Controls
## Virtual Environment
### Requirements
* virtualenv2

```sh
$ cd car_controls
$ ./config.py setup                 # setup virtual environment
$ ./config.py install               # installing all requirements in requirements.txt
$ source ../cc_venv/bin/activate    # activate virtual environment
...
(cc_venv)$ deactivate               # for deactivating virtual environment
```
for more --> https://virtualenv.pypa.io/en/stable/userguide/
## mbed-cli
### Requirements
* arm-none-eabi-gcc
* git
* mercurial
* arm-none-eabi-newlib (arch)

Make sure cc_venv is activated!
```sh
(cc_venv)$ mbed deploy              			# adds mbed library to project + installs mbed 2.0 SDK tools (time for a coffee!)
(cc_venv)$ mbed compile 				# compiles sourcecode and generates elf & bin files
# bin file can now be flashed to the nucleo
# bin located at BUILD/NUCLEO_F303K8/GCC_ARM/car_controls.bin
...
(cc_venv)$ rm -r .temp/            			# otherwise the following line is NOT POSSIBLE
(cc_venv)$ mbed detect              			# lists all connected mbed devices
```
for more --> https://github.com/ARMmbed/mbed-cli


## Common Errors
*Unknown command 'mbed'*
* you need to install the virtualenv and activate it

*ImportError: No module named test_configs* when mbed detect
* you need to remove the .temp/ folder
