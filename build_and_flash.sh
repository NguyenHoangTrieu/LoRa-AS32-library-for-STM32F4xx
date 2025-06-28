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
sudo "$PROGRAMMER" -c port=SWD sn=52FF6F064849825057460467 -w Sender_demo.bin 0x08000000 -v -rst
sudo "$PROGRAMMER" -c port=SWD sn=52FF71064849825056350467 -w Sender_demo.bin 0x08000000 -v -rst
sudo "$PROGRAMMER" -c port=SWD sn=52FF6D064849825053310667 -w Sender_demo.bin 0x08000000 -v -rst
sudo "$PROGRAMMER" -c port=SWD sn=52FF6E064849825043360667 -w Sender_demo.bin 0x08000000 -v -rst
sudo "$PROGRAMMER" -c port=SWD sn=52FF6C064849825033360667 -w Sender_demo.bin 0x08000000 -v -rst
# List available serial ports
echo "---------------------------------------------"
echo "Available serial ports:"
echo "---------------------------------------------"
echo "Available serial ports:"
ls /dev/ttyUSB*

cd ../../..
pytest -s test_uart.py