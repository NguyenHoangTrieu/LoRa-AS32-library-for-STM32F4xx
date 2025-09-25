cd Examples/Sender
rmdir /S /Q build
mkdir build
cd build
cmake -G Ninja -DCMAKE_TOOLCHAIN_FILE=../../arm-none-eabi-gcc.cmake ..
ninja
STM32_Programmer_CLI -c port=SWD sn=52FF6C064849825033360667 -w Sender_demo.bin 0x08000000 -v -rst