# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

from distutils.sysconfig import get_python_inc
import platform
import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
    '-Wall',
    #'-Wextra',
    #'-Werror',
    '-Wno-long-long',
    '-Wno-variadic-macros',
    '-fexceptions',
    '-DNDEBUG',
    # You 100% do NOT need -DUSE_CLANG_COMPLETER in your flags; only the YCM
    # source code needs it.
    '-DUSE_CLANG_COMPLETER',
    # THIS IS IMPORTANT! Without the '-x' flag, Clang won't know which language to
    # use when compiling headers. So it will guess. Badly. So C++ headers will be
    # compiled as C headers. You don't want that so ALWAYS specify the '-x' flag.
    # For a C project, you would set this to 'c' instead of 'c++'.
    '-x',
    'c++',
    '-isystem', '../BoostParts',
    '-isystem', get_python_inc(),
    '-isystem', '../llvm/include',
    '-isystem', '../llvm/tools/clang/include',
    '-isystem', './tests/gmock/gtest',
    '-isystem', './tests/gmock/gtest/include',
    '-isystem', './tests/gmock',
    '-isystem', './tests/gmock/include',
    '-isystem', './benchmarks/benchmark/include',
    '-I', './ClangCompleter',
    '-I', '/usr/include/c++/7.2.1',
    '-I', '/usr/include',
    '-I', 'mbed/fb8e0ae1cceb',
    '-I', 'servo',
    '-I', '.',

    #config
    '-DMBED_CONF_PLATFORM_STDIO_BAUD_RATE=9600',
    '-DCLOCK_SOURCE=USE_PLL_HSI',
    '-DMBED_CONF_PLATFORM_DEFAULT_SERIAL_BAUD_RATE=9600',
    '-DMBED_CONF_PLATFORM_STDIO_FLUSH_AT_EXIT=1',
    '-DMBED_CONF_PLATFORM_STDIO_CONVERT_NEWLINES=0',

    #mbed C flags
    '-std=gnu99',
    '-D__MBED__=1',
    '-DDEVICE_I2CSLAVE=1',
    '-D__FPU_PRESENT=1',
    '-DDEVICE_PORTOUT=1',
    '-DDEVICE_PORTINOUT=1',
    '-DTARGET_RTOS_M4_M7',
    '-DDEVICE_LOWPOWERTIMER=1',
    '-DMBED_BUILD_TIMESTAMP=1509975672.86',
    '-DTARGET_STM32F303K8',
    '-DTARGET_NUCLEO_F303K8',
    '-D__CMSIS_RTOS',
    '-DTOOLCHAIN_GCC',
    '-DDEVICE_STDIO_MESSAGES=1',
    '-DDEVICE_CAN=1',
    '-DTARGET_CORTEX_M',
    '-DDEVICE_I2C_ASYNCH=1',
    '-DTARGET_LIKE_CORTEX_M4',
    '-DDEVICE_ANALOGOUT=1',
    '-DTARGET_M4',
    '-DTARGET_UVISOR_UNSUPPORTED',
    '-DTARGET_STM32F303x8',
    '-DDEVICE_SERIAL=1',
    '-DDEVICE_SPI_ASYNCH=1',
    '-DDEVICE_INTERRUPTIN=1',
    '-DTARGET_CORTEX',
    '-DDEVICE_I2C=1',
    '-DTRANSACTION_QUEUE_SIZE_SPI=2',
    '-DRTC_LSI=1',
    '-D__CORTEX_M4',
    '-D__MBED_CMSIS_RTOS_CM',
    '-DTARGET_FAMILY_STM32',
    '-DTARGET_FF_ARDUINO',
    '-DDEVICE_PORTIN=1',
    '-DTARGET_RELEASE',
    '-DTARGET_STM',
    '-DDEVICE_SERIAL_FC=1',
    '-DTARGET_LIKE_MBED',
    '-DTARGET_STM32F3',
    '-DDEVICE_SLEEP=1',
    '-DTOOLCHAIN_GCC_ARM',
    '-DDEVICE_SPI=1',
    '-DDEVICE_SPISLAVE=1',
    '-DDEVICE_ANALOGIN=1',
    '-DDEVICE_PWMOUT=1',
    '-DDEVICE_RTC=1',
    '-DARM_MATH_CM4',
    '-DTOOLCHAIN_object',
    '-include', 'mbed_config.h',

    # mbed CXX flags
    '-std=gnu++98',
    '-fno-rtti',
    '-Wvla',
    '-D__MBED__=1',
    '-DDEVICE_I2CSLAVE=1',
    '-D__FPU_PRESENT=1',
    '-DDEVICE_PORTOUT=1',
    '-DDEVICE_PORTINOUT=1',
    '-DTARGET_RTOS_M4_M7',
    '-DDEVICE_LOWPOWERTIMER=1',
    '-DMBED_BUILD_TIMESTAMP=1509975672.86',
    '-DTARGET_STM32F303K8',
    '-DTARGET_NUCLEO_F303K8',
    '-D__CMSIS_RTOS',
    '-DTOOLCHAIN_GCC',
    '-DDEVICE_STDIO_MESSAGES=1',
    '-DDEVICE_CAN=1',
    '-DTARGET_CORTEX_M',
    '-DDEVICE_I2C_ASYNCH=1',
    '-DTARGET_LIKE_CORTEX_M4',
    '-DDEVICE_ANALOGOUT=1',
    '-DTARGET_M4',
    '-DTARGET_UVISOR_UNSUPPORTED',
    '-DTARGET_STM32F303x8',
    '-DDEVICE_SERIAL=1',
    '-DDEVICE_SPI_ASYNCH=1',
    '-DDEVICE_INTERRUPTIN=1',
    '-DTARGET_CORTEX',
    '-DDEVICE_I2C=1',
    '-DTRANSACTION_QUEUE_SIZE_SPI=2',
    '-DRTC_LSI=1',
    '-D__CORTEX_M4',
    '-D__MBED_CMSIS_RTOS_CM',
    '-DTARGET_FAMILY_STM32',
    '-DTARGET_FF_ARDUINO',
    '-DDEVICE_PORTIN=1',
    '-DTARGET_RELEASE',
    '-DTARGET_STM',
    '-DDEVICE_SERIAL_FC=1',
    '-DTARGET_LIKE_MBED',
    '-DTARGET_STM32F3',
    '-DDEVICE_SLEEP=1',
    '-DTOOLCHAIN_GCC_ARM',
    '-DDEVICE_SPI=1',
    '-DDEVICE_SPISLAVE=1',
    '-DDEVICE_ANALOGIN=1',
    '-DDEVICE_PWMOUT=1',
    '-DDEVICE_RTC=1',
    '-DARM_MATH_CM4',
    '-DTOOLCHAIN_object',
    '-include mbed_config.h'
    '-include mbed_config.h',

    # mbed ASM flags
    '-DTRANSACTION_QUEUE_SIZE_SPI=2',
    '-DRTC_LSI=1',
    '-D__CORTEX_M4',
    '-DARM_MATH_CM4',
    '-D__FPU_PRESENT=1',
    '-D__MBED_CMSIS_RTOS_CM',
    '-D__CMSIS_RTOS',
    '-I', 'mbed/.',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TARGET_STM',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TARGET_STM/TARGET_STM32F3',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TARGET_STM/TARGET_STM32F3/TARGET_STM32F303x8',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TARGET_STM/TARGET_STM32F3/TARGET_STM32F303x8/TARGET_NUCLEO_F303K8',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TARGET_STM/TARGET_STM32F3/TARGET_STM32F303x8/device',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TARGET_STM/TARGET_STM32F3/device',
    '-I', 'mbed/fb8e0ae1cceb/TARGET_NUCLEO_F303K8/TOOLCHAIN_GCC_ARM',
    '-I', 'mbed/fb8e0ae1cceb/drivers',
    '-I', 'mbed/fb8e0ae1cceb/hal',
    '-I', 'mbed/fb8e0ae1cceb/platform',
]

# Clang automatically sets the '-std=' flag to 'c++14' for MSVC 2015 or later,
# which is required for compiling the standard library, and to 'c++11' for older
# versions.
if platform.system() != 'Windows':
  flags.append( '-std=c++17' )


# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# You can get CMake to generate this file for you by adding:
#   set( CMAKE_EXPORT_COMPILE_COMMANDS 1 )
# to your CMakeLists.txt file.
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    basename = os.path.splitext( filename )[ 0 ]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )


def FlagsForFile( filename, **kwargs ):
  if not database:
    return {
      'flags': flags,
      'include_paths_relative_to_dir': DirectoryOfThisScript()
    }

  compilation_info = GetCompilationInfoForFile( filename )
  if not compilation_info:
    return None

  # Bear in mind that compilation_info.compiler_flags_ does NOT return a
  # python list, but a "list-like" StringVec object.
  final_flags = list( compilation_info.compiler_flags_ )

  # NOTE: This is just for YouCompleteMe; it's highly likely that your project
  # does NOT need to remove the stdlib flag. DO NOT USE THIS IN YOUR
  # ycm_extra_conf IF YOU'RE NOT 100% SURE YOU NEED IT.
  try:
    final_flags.remove( '-stdlib=libc++' )
  except ValueError:
    pass

  return {
    'flags': final_flags,
    'include_paths_relative_to_dir': compilation_info.compiler_working_dir_
  }
