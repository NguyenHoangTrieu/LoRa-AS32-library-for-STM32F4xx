#!/bin/bash

set -e  # Dừng script nếu có lỗi
echo "---------------------------------------------"
echo "Build and flash the Sender example to board:"
echo "---------------------------------------------"
cd Examples/Sender
rm -rf build
mkdir build
cd build
cmake -G Ninja -DCMAKE_TOOLCHAIN_FILE=../../arm-none-eabi-gcc.cmake ..
ninja
PROGRAMMER="/home/trieunguyen/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
echo "[INFO] Flashing firmware..."
# Flash Node 001
sudo "$PROGRAMMER" -c port=SWD sn=52FF6F064849825057460467 -w Node_01.bin 0x08000000 -v -rst