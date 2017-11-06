# Car Controls
## Virtual Environment
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
Make sure cc_venv is activated!
```sh
(cc_venv)$ mbed deploy              			# adds mbed library to project + installs mbed 2.0 SDK tools (time for a coffee!)
(cc_venv)$ mbed compile 				# compiles sourcecode and generates elf & bin files
# bin file can now be flashed to the nucleo
...
(cc_venv)$ rm -r .temp/            			# otherwise the following line is NOT POSSIBLE
(cc_venv)$ mbed detect              			# lists all connected mbed devices
```
for more --> https://github.com/ARMmbed/mbed-cli
