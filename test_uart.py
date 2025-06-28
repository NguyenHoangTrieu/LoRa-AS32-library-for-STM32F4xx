import pytest
import serial
import serial.tools.list_ports
import time
import sys
from datetime import datetime

# Ensure stdout uses UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

def get_available_ports():
    """Retrieve a list of available serial ports."""
    return [port.device for port in serial.tools.list_ports.comports()]

@pytest.fixture(scope="module")
def uart_usb0():
    """Open /dev/ttyUSB0 (Gateway) at 19200 baud rate if available."""
    if "/dev/ttyUSB0" not in get_available_ports():
        pytest.skip("/dev/ttyUSB0 is not available!")

    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=19200, timeout=1)
    print(f"Connected to: {ser.name}")
    yield ser
    ser.close()

@pytest.fixture(scope="module")
def uart_usb1():
    """Open /dev/ttyUSB1 (Test_Node) at 19200 baud rate if available."""
    if "/dev/ttyUSB1" not in get_available_ports():
        pytest.skip("/dev/ttyUSB1 is not available!")

    ser = serial.Serial(port="/dev/ttyUSB1", baudrate=19200, timeout=1)
    print(f"Connected to: {ser.name}")
    yield ser
    ser.close()

@pytest.fixture(scope="module")
def uart_usb2():
    """Open /dev/ttyUSB2 (Node_02) at 19200 baud rate if available."""
    if "/dev/ttyUSB2" not in get_available_ports():
        pytest.skip("/dev/ttyUSB2 is not available!")

    ser = serial.Serial(port="/dev/ttyUSB2", baudrate=19200, timeout=1)
    print(f"Connected to: {ser.name}")
    yield ser
    ser.close()

def test_uart_read(uart_usb0, uart_usb1, uart_usb2):
    """Read data from all devices for 60 seconds, group bursts, and print at the end."""
    start_time = time.time()
    timeout = 60  # seconds

    burst_timeout_0 = 0.01
    burst_timeout_1 = 0.005
    burst_timeout_2 = 0.01

    buffer_0, buffer_1, buffer_2 = "", "", ""
    last_rx_0 = last_rx_1 = last_rx_2 = time.time()

    log_0, log_1, log_2 = [], [], []

    while time.time() - start_time < timeout:
        now = time.time()

        # USB0 (Gateway)
        if uart_usb0.in_waiting:
            data = uart_usb0.read(uart_usb0.in_waiting).decode("utf-8", errors="ignore")
            buffer_0 += data
            last_rx_0 = now
        elif buffer_0 and (now - last_rx_0) > burst_timeout_0:
            log_0.append(f"[{datetime.now().strftime('%H:%M:%S:%f')[:-3]}] {buffer_0.strip()}")
            buffer_0 = ""

        # USB1 (Test_Node)
        if uart_usb1.in_waiting:
            data = uart_usb1.read(uart_usb1.in_waiting).decode("utf-8", errors="ignore")
            buffer_1 += data
            last_rx_1 = now
        elif buffer_1 and (now - last_rx_1) > burst_timeout_1:
            log_1.append(f"[{datetime.now().strftime('%H:%M:%S:%f')[:-3]}] {buffer_1.strip()}")
            buffer_1 = ""

        # USB2 (Node_02)
        if uart_usb2.in_waiting:
            data = uart_usb2.read(uart_usb2.in_waiting).decode("utf-8", errors="ignore")
            buffer_2 += data
            last_rx_2 = now
        elif buffer_2 and (now - last_rx_2) > burst_timeout_2:
            log_2.append(f"[{datetime.now().strftime('%H:%M:%S:%f')[:-3]}] {buffer_2.strip()}")
            buffer_2 = ""

    # Print results
    if log_0:
        print("USB0 (Test1):")
        for entry in log_0:
            print(entry)

    if log_1:
        print("USB1 (Test2):")
        for entry in log_1:
            print(entry)

    if log_2:
        print("USB2 (Test3):")
        for entry in log_2:
            print(entry)

    print("Data collection complete.")
    assert True  # So pytest does not mark test as fail
