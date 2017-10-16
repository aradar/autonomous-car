# car controls for selfdriving rc car
## board
* [Nucleo F303K8](http://www.st.com/en/evaluation-tools/nucleo-f303k8.html) 

## project setup
* clion as ide
* [ozone as debugger (jlink)](https://goo.gl/ArnuzH)
* cmake as build tool
* gnu gcc for ARM (gcc-arm-none-eabi) as compiler
* [STM32CubeMX](https://goo.gl/fN3AZF) for code generation
### CMake settings:
* Configuration:	Debug
* CMake options: 	-DCMAKE_TOOLCHAIN_FILE=STM32F303x8.cmake
* Generation path: 	build
### Run/Debug Configurations:
* Target: 		All targets
* Configuration: 	Debug
* Executable:		Ozone
* Program arguments: 	run.jdebug
* Working Directory: 	{path_to_project}/car_controls
### Ozone settings:
* New Project Wizard
 * Device:		STM32F303K8
 * Peripherals:		-
 * Target Interface: 	8 MHz (1M Hz, 4 MHz also working)
 * Host Interface:	USB
 * Serial No:		-
 * Binary file:		{path_to_elf_file}.elf

## converted st-link on-board into j-link debugger:
* https://goo.gl/Q71J2X

## jetbrains cmake embedded development tutorial
* https://blog.jetbrains.com/clion/2016/06/clion-for-embedded-development/
