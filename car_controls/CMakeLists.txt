project(car_controls C ASM)
cmake_minimum_required(VERSION 3.5.0)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_VERBOSE_MAKEFILE ON)

add_definitions(-DSTM32F303x8)

file(GLOB_RECURSE USER_SOURCES "Src/*.c")
# file(GLOB_RECURSE HAL_SOURCES "Drivers/STM32F3xx_HAL_Driver/Src/*.c")

set(HAL_SOURCES 
		Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal.c
		Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_rcc.c
		Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_cortex.c
		Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_gpio.c
		)

add_library(CMSIS
        Src/system_stm32f3xx.c
        startup/startup_stm32f303x8.s)

include_directories(Inc
                    Drivers/CMSIS/Include
                    Drivers/CMSIS/Device/ST/STM32F3xx/Include
                    Drivers/STM32F3xx_HAL_Driver/Inc
                    Drivers/STM32F3xx_Nucleo_32)

add_executable(${PROJECT_NAME}.elf ${USER_SOURCES} Drivers/STM32F3xx_Nucleo_32/stm32f3xx_nucleo_32.c ${HAL_SOURCES} ${LINKER_SCRIPT})
target_link_libraries(${PROJECT_NAME}.elf CMSIS)

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Map=${CMAKE_BINARY_DIR}/${PROJECT_NAME}.map")
set(HEX_FILE ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.hex)
set(BIN_FILE ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.bin)
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -Oihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
        COMMAND ${CMAKE_OBJCOPY} -Obinary $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
        COMMENT "Building ${HEX_FILE} \nBuilding ${BIN_FILE}")
