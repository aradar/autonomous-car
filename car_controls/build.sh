#!/bin/bash

function print_usage()
{
	echo "build:"
	echo "   before calling this script, cd into build-dir!"
	echo "   -h              help"
	echo "   <without-args>  build"
	echo "   -a              call cmake and build"
	echo "   -c              clear build-dir"
}

if [ "$1" == "-h" ]; then
	print_usage
	exit 0
fi

# in build dir?
if [[ $PWD != */build ]]; then 		# not in build
	echo "ERROR: cd into build-dir and then call this script!!"
	exit 1
fi

# to clean up build-dir
function try_rm()
{
	if [ -f $1 ]; then
		rm $1
	fi
}

# clear build dir
try_rm car_controls.bin
try_rm car_controls.elf
try_rm car_controls.hex
try_rm car_controls.map

# clear
if [ "$1" == "-c" ]; then
	exit 0
fi

# cmake
# if flag "-a" is set or file "./Makefile" does not exists
if [ "$1" == "-a" || ! -f "./Makefile" ]; then
	echo "CALLING cmake"
	cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=STM32F303x8.cmake -G "CodeBlocks - Unix Makefiles" ../
fi

# print error
err=$?
if [[ $err -ne 0 ]]; then
	echo "ERROR: cmake failed! error-code: $err"
	exit 1
fi

# make
echo "CALLING make"
make -f CMakeFiles/Makefile2 all

# print error
err=$?
if [[ $err -eq 127 ]]; then # if "make" not found, try "mingw32-make" for our windows users :)
	mingw32-make -f CMakeFiles/Makefile2 all
else
	if [[ $err -ne 0 ]]; then
		echo "ERROR: make failed! error-code: $err"
		exit 1
	fi
fi
