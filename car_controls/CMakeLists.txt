project (car_controls C CXX ASM)
cmake_minimum_required(VERSION 3.8)

set(SOURCE_FILES main.cpp)

include_directories(mbed/*.h)

add_executable(car_controls ${SOURCE_FILES})