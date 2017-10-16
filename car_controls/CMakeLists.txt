project(car_controls C ASM)
cmake_minimum_required(VERSION 3.5.0)
set(CMAKE_CXX_STANDARD 11)

add_definitions(-DSTM32F303x8)

set(SOURCE_FILES
        Drivers/CMSIS/Device/ST/STM32F3xx/Include/stm32f303x8.h
        Drivers/CMSIS/Device/ST/STM32F3xx/Include/stm32f3xx.h
        Drivers/CMSIS/Device/ST/STM32F3xx/Include/system_stm32f3xx.h
        Drivers/CMSIS/Include/arm_common_tables.h
        Drivers/CMSIS/Include/arm_const_structs.h
        Drivers/CMSIS/Include/arm_math.h
        Drivers/CMSIS/Include/cmsis_armcc.h
        Drivers/CMSIS/Include/cmsis_armcc_V6.h
        Drivers/CMSIS/Include/cmsis_gcc.h
        Drivers/CMSIS/Include/core_cm0.h
        Drivers/CMSIS/Include/core_cm0plus.h
        Drivers/CMSIS/Include/core_cm3.h
        Drivers/CMSIS/Include/core_cm4.h
        Drivers/CMSIS/Include/core_cm7.h
        Drivers/CMSIS/Include/core_cmFunc.h
        Drivers/CMSIS/Include/core_cmInstr.h
        Drivers/CMSIS/Include/core_cmSimd.h
        Drivers/CMSIS/Include/core_sc000.h
        Drivers/CMSIS/Include/core_sc300.h
        Drivers/STM32F3xx_HAL_Driver/Inc/Legacy/stm32_hal_legacy.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_cortex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_def.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_dma.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_dma_ex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_flash.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_flash_ex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_gpio.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_gpio_ex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_i2c.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_i2c_ex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_pwr.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_pwr_ex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_rcc.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_rcc_ex.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_tim.h
        Drivers/STM32F3xx_HAL_Driver/Inc/stm32f3xx_hal_tim_ex.h
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_cortex.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_dma.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_flash.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_flash_ex.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_gpio.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_i2c.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_i2c_ex.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_pwr.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_pwr_ex.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_rcc.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_rcc_ex.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_tim.c
        Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_tim_ex.c
        Drivers/STM32F3xx_Nucleo_32/stm32f3xx_nucleo_32.c
        Drivers/STM32F3xx_Nucleo_32/stm32f3xx_nucleo_32.h
        Inc/main.h
        Inc/stm32f3xx_hal_conf.h
        Inc/stm32f3xx_it.h
        Src/main.c
        Src/stm32f3xx_hal_msp.c
        Src/stm32f3xx_it.c
        Src/system_stm32f3xx.c
        startup/startup_stm32f303x8.s
        please_blink_boi.ioc
        STM32F303K8Tx_FLASH.ld)

file(GLOB_RECURSE USER_SOURCES "Src/*.c")
file(GLOB_RECURSE HAL_SOURCES "Drivers/STM32F3xx_HAL_Driver/Src/*.c")

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

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Map=${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME}.map")
set(HEX_FILE ${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME}.hex)
set(BIN_FILE ${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME}.bin)
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -Oihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
        COMMAND ${CMAKE_OBJCOPY} -Obinary $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
        COMMENT "Building ${HEX_FILE} \nBuilding ${BIN_FILE}")
