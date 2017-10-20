#!/bin/bash
if [ "$1" == "-c" ]; then
	cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=STM32F303x8.cmake -G "CodeBlocks - Unix Makefiles" ../
fi
make -f CMakeFiles/Makefile2 all
